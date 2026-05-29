import time
from datetime import datetime

from pyspark.sql import SparkSession

from src.config.project_config import (
    STORAGE_CONFIG
)

from src.utils.storage.delta_io import (
    read_table,
    merge_table
)

from src.utils.monitoring.pipeline_logger import (
    PipelineLogger
)

from src.utils.quality.runner import (
    run_quality_checks
)

from src.star.registry.dimensions import (
    STAR_DIMENSIONS,
    DIMENSIONS_EXECUTION_ORDER
)

from src.star.registry.facts import (
    STAR_FACTS,
    FACTS_EXECUTION_ORDER
)


LAYER = "star"

STAR_OBJECTS = {
    **STAR_DIMENSIONS,
    **STAR_FACTS
}

STAR_EXECUTION_ORDER = [
    *DIMENSIONS_EXECUTION_ORDER,
    *FACTS_EXECUTION_ORDER
]

def _now() -> str:
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def _print_step(
    dataset: str,
    message: str
) -> None:
    """Print a simple execution message for the Star pipeline."""
    print(
        f"[{_now()}] [STAR] [{dataset}] {message}",
        flush=True
    )


def _resolver_datasets(
    object_name: str | list[str] = "all"
) -> list[str]:
    """Resolve the Star objects that should be processed."""

    if object_name == "all":

        return STAR_EXECUTION_ORDER

    if isinstance(
        object_name,
        str
    ):

        return [
            object_name
        ]

    return list(
        object_name
    )


def _validar_objeto(
    object_name: str,
    logger: PipelineLogger
) -> bool:

    if object_name not in STAR_OBJECTS:

        message = (
            "Objeto não registrado em STAR_OBJECTS"
        )

        _print_step(
            object_name,
            f"AVISO: {message}"
        )

        logger.log_warning(
            LAYER,
            object_name,
            message
        )

        return False

    return True


def _parse_source(
    source: str
) -> tuple[str, str]:
    """Split a source reference into layer and table name."""

    if "." not in source:

        return "gold", source

    parts = source.split(
        ".",
        1
    )

    return parts[0], parts[1]


def _carregar_fontes(
    spark,
    object_name: str,
    sources: list
):

    dfs = {}

    for source in sources:

        layer, table_name = _parse_source(
            source
        )

        _print_step(
            object_name,
            f"Lendo {layer}.{table_name}"
        )

        dfs[source] = read_table(
            spark=spark,
            storage_config=STORAGE_CONFIG,
            layer=layer,
            table_name=table_name
        )

        _print_step(
            object_name,
            f"Fonte {layer}.{table_name} carregada"
        )

    return dfs


def _executar_funcao_transform(
    fn,
    dfs: dict,
    sources: list
):

    args = [
        dfs[source]
        for source in sources
    ]

    return fn(
        *args
    )


def run_star(
    object_name: str | list[str] = "all"
) -> None:
    """Run the Star pipeline for one object, a list of objects or all objects."""

    spark = SparkSession.builder.getOrCreate()

    logger = PipelineLogger(
        spark=spark,
        log_path=STORAGE_CONFIG["logs"]
    )

    objects = _resolver_datasets(
        object_name
    )

    total_objects = len(
        objects
    )

    print(
        "\n"
        "==================================================\n"
        "INICIANDO PIPELINE STAR SCHEMA\n"
        f"Objetos: {objects}\n"
        f"Total objetos: {total_objects}\n"
        f"Execution ID: {logger.execution_id}\n"
        "==================================================\n",
        flush=True
    )

    pipeline_start = time.time()

    for index, obj in enumerate(
        objects,
        start=1
    ):

        obj_start = time.time()

        _print_step(
            obj,
            f"Iniciando objeto {index}/{total_objects}"
        )

        if not _validar_objeto(
            obj,
            logger
        ):

            _print_step(
                obj,
                "Pulando objeto por falha de validação"
            )

            continue

        cfg = STAR_OBJECTS[
            obj
        ]

        fn = cfg["fn"]

        target_table = cfg["table"]

        merge_keys = cfg["merge_keys"]

        sources = cfg["sources"]

        try:

            logger.log_start(
                LAYER,
                obj
            )

            logger.log_info(
                LAYER,
                obj,
                f"Tabela destino: {target_table}"
            )

            logger.log_info(
                LAYER,
                obj,
                f"Fontes: {sources}"
            )

            logger.log_info(
                LAYER,
                obj,
                f"Merge keys: {merge_keys}"
            )

            # ======================================
            # READ SOURCES
            # ======================================

            read_start = time.time()

            dfs = _carregar_fontes(
                spark=spark,
                object_name=obj,
                sources=sources
            )

            read_duration = time.time() - read_start

            _print_step(
                obj,
                f"Fontes carregadas em {read_duration:.1f}s"
            )

            logger.log_event(
                LAYER,
                obj,
                "READ_SOURCES_SUCCESS",
                "Fontes carregadas com sucesso"
            )

            # ======================================
            # TRANSFORM
            # ======================================

            _print_step(
                obj,
                "Iniciando transformação star"
            )

            transform_start = time.time()

            df_star = _executar_funcao_transform(
                fn=fn,
                dfs=dfs,
                sources=sources
            )

            df_star.cache()

            record_count = df_star.count()

            transform_duration = (
                time.time()
                - transform_start
            )

            _print_step(
                obj,
                f"Transformação concluída com {record_count} registros "
                f"em {transform_duration:.1f}s"
            )

            logger.log_event(
                LAYER,
                obj,
                "TRANSFORM_SUCCESS",
                "Transformação star concluída",
                records=record_count
            )

            quality_results = run_quality_checks(
                df=df_star,
                layer=LAYER,
                table_name=target_table,
                fail_on_error=True
            )

            if quality_results:

                failed_quality_checks = [
                    result
                    for result in quality_results
                    if result["status"] == "failed"
                ]

                logger.log_event(
                    LAYER,
                    obj,
                    "DATA_QUALITY_SUCCESS",
                    (
                        "Validações de Data Quality executadas: "
                        f"{len(quality_results)} regras, "
                        f"{len(failed_quality_checks)} falhas não bloqueantes"
                    ),
                    records=record_count
                )

            if record_count == 0:

                message = (
                    "DataFrame star vazio após transformação"
                )

                _print_step(
                    obj,
                    f"AVISO: {message}"
                )

                logger.log_warning(
                    LAYER,
                    obj,
                    message
                )

                df_star.unpersist()

                continue

            # ======================================
            # WRITE STAR
            # ======================================

            _print_step(
                obj,
                f"Gravando {LAYER}.{target_table} "
                f"com merge_keys={merge_keys}"
            )

            write_start = time.time()

            merge_table(
                spark=spark,
                df=df_star,
                storage_config=STORAGE_CONFIG,
                layer=LAYER,
                table_name=target_table,
                merge_keys=merge_keys
            )

            write_duration = (
                time.time()
                - write_start
            )

            _print_step(
                obj,
                f"Gravação concluída em {write_duration:.1f}s"
            )

            logger.log_event(
                LAYER,
                obj,
                "WRITE_STAR_SUCCESS",
                f"{LAYER}.{target_table} gravada com sucesso",
                records=record_count
            )

            # ======================================
            # SUCCESS
            # ======================================

            obj_duration = (
                time.time()
                - obj_start
            )

            logger.log_success(
                LAYER,
                obj,
                record_count
            )

            _print_step(
                obj,
                f"Objeto concluído com sucesso em {obj_duration:.1f}s"
            )

            df_star.unpersist()

        except Exception as exc:

            obj_duration = (
                time.time()
                - obj_start
            )

            _print_step(
                obj,
                f"ERRO após {obj_duration:.1f}s: "
                f"{type(exc).__name__}: {exc}"
            )

            logger.log_error(
                LAYER,
                obj,
                "Falha no processamento star",
                exc
            )

            raise

    pipeline_duration = (
        time.time()
        - pipeline_start
    )

    print(
        "\n"
        "==================================================\n"
        "PIPELINE STAR SCHEMA FINALIZADO\n"
        f"Duração total: {pipeline_duration:.1f}s\n"
        f"Execution ID: {logger.execution_id}\n"
        "==================================================\n",
        flush=True
    )

if __name__ == "__main__":
    run_star()
