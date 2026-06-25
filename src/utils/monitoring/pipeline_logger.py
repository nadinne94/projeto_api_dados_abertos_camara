"""
Logging estruturado para execução dos pipelines.

Centraliza a geração de logs operacionais com identificador de execução,
camada, tabela, status, mensagens e métricas de processamento.

Este módulo apoia a rastreabilidade das execuções e pode persistir os
registros em Delta Lake.
"""

import logging

from uuid import uuid4
from typing import Optional

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import (
    LongType,
    StringType,
    StructField,
    StructType,
)

logger = logging.getLogger(__name__)

LOG_SCHEMA = StructType([

    StructField(
        "execution_id",
        StringType(),
        True
    ),

    StructField(
        "layer",
        StringType(),
        True
    ),

    StructField(
        "dataset",
        StringType(),
        True
    ),

    StructField(
        "status",
        StringType(),
        True
    ),

    StructField(
        "message",
        StringType(),
        True
    ),

    StructField(
        "records",
        LongType(),
        True
    )
])


class PipelineLogger:

    """
    Logger estruturado persistido em Delta.
    """

    def __init__(
        self,
        spark: SparkSession,
        log_path: str
    ):

        self.spark = spark

        self.log_path = log_path

        self.execution_id = str(
            uuid4()
        )

    def _write_delta(
        self,
        layer: str,
        dataset: str,
        status: str,
        message: Optional[str] = None,
        records: Optional[int] = None
    ) -> None:

        try:

            df = (

                self.spark.createDataFrame(

                    [(
                        self.execution_id,
                        layer,
                        dataset,
                        status,
                        message,
                        int(records) if records is not None else None
                    )],

                    schema=LOG_SCHEMA

                )

                .withColumn(
                    "timestamp",
                    current_timestamp()
                )

            )

            (

                df.write
                .format("delta")
                .mode("append")
                .save(self.log_path)

            )

        except Exception as exc:

            logger.error(
                "Falha Delta log: %s",
                exc
            )

    def _write_python_log(
        self,
        status: str,
        layer: str,
        dataset: str,
        message: Optional[str]
    ) -> None:

        log_message = (

            f"[{status}] "

            f"{layer}.{dataset} "

            f"- {message}"

        )

        status = status.upper()

        if status == "ERROR":

            logger.error(log_message)

        elif status == "WARNING":

            logger.warning(log_message)

        else:

            logger.info(log_message)

    def log_event(
        self,
        layer: str,
        dataset: str,
        status: str,
        message: Optional[str] = None,
        records: Optional[int] = None,
        persist: bool = True
    ) -> None:

        self._write_python_log(
            status,
            layer,
            dataset,
            message
        )

        if persist:

            self._write_delta(
                layer,
                dataset,
                status,
                message,
                records
            )

    def log_start(
        self,
        layer: str,
        dataset: str
    ):

        self.log_event(
            layer,
            dataset,
            "START",
            "Processamento iniciado"
        )

    def log_success(
        self,
        layer: str,
        dataset: str,
        records: Optional[int] = None
    ):

        self.log_event(
            layer,
            dataset,
            "SUCCESS",
            "Processamento concluído",
            records
        )

    def log_info(
        self,
        layer: str,
        dataset: str,
        message: str,
        persist: bool = False
    ):

        self.log_event(
            layer,
            dataset,
            "INFO",
            message,
            persist=persist
        )

    def log_warning(
        self,
        layer: str,
        dataset: str,
        message: str
    ):

        self.log_event(
            layer,
            dataset,
            "WARNING",
            message
        )

    def log_error(
        self,
        layer: str,
        dataset: str,
        message: str,
        exc: Optional[Exception] = None
    ):

        final_message = message

        if exc:

            final_message = (

                f"{message}"

                f" | "

                f"{type(exc).__name__}: {exc}"

            )

        self.log_event(
            layer,
            dataset,
            "ERROR",
            final_message
        )