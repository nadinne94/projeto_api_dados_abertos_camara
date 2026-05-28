"""
Runner de Data Quality.

Este módulo executa contratos declarativos de qualidade sobre DataFrames
Spark e decide se falhas devem bloquear ou apenas gerar warnings.
"""

from typing import Dict, List

from pyspark.sql import DataFrame

from src.utils.quality.checks import (
    check_allowed_values,
    check_max_null_ratio,
    check_no_nulls,
    check_not_empty,
    check_required_columns,
    check_unique_key
)
from src.utils.quality.contracts import DATA_QUALITY_CONTRACTS


def run_quality_checks(
    df: DataFrame,
    layer: str,
    table_name: str,
    fail_on_error: bool = True
) -> List[dict]:
    """
    Executa as validações de Data Quality para uma tabela.

    Args:
        df: DataFrame a ser validado.
        layer: Camada do pipeline. Exemplo: bronze, silver, gold, star.
        table_name: Nome da tabela/dataset.
        fail_on_error: Se True, lança exceção quando houver falha com
            severidade error.

    Returns:
        Lista de resultados das regras executadas.

    Raises:
        ValueError: Se houver falhas bloqueantes e fail_on_error=True.
    """

    contract = (
        DATA_QUALITY_CONTRACTS
        .get(layer, {})
        .get(table_name)
    )

    if not contract:
        return []

    results = []

    if "not_empty" in contract:
        rule = contract["not_empty"]

        results.append(
            check_not_empty(
                df=df,
                severity=rule.get("severity", "error")
            )
        )

    if "required_columns" in contract:
        rule = contract["required_columns"]

        results.append(
            check_required_columns(
                df=df,
                required_columns=rule["columns"],
                severity=rule.get("severity", "error")
            )
        )

    if "no_nulls" in contract:
        rule = contract["no_nulls"]

        results.append(
            check_no_nulls(
                df=df,
                columns=rule["columns"],
                severity=rule.get("severity", "error")
            )
        )

    if "unique_key" in contract:
        rule = contract["unique_key"]

        results.append(
            check_unique_key(
                df=df,
                key_columns=rule["columns"],
                severity=rule.get("severity", "error")
            )
        )

    if "max_null_ratio" in contract:
        rule = contract["max_null_ratio"]

        results.append(
            check_max_null_ratio(
                df=df,
                column_name=rule["column"],
                max_ratio=rule["max_ratio"],
                severity=rule.get("severity", "warning")
            )
        )

    if "allowed_values" in contract:
        rule = contract["allowed_values"]

        results.append(
            check_allowed_values(
                df=df,
                column_name=rule["column"],
                allowed_values=rule["values"],
                severity=rule.get("severity", "error")
            )
        )

    failed_errors = [
        result
        for result in results
        if result["status"] == "failed"
        and result["severity"] == "error"
    ]

    if failed_errors and fail_on_error:
        messages = [
            result["message"]
            for result in failed_errors
        ]

        raise ValueError(
            "Falha em validações críticas de Data Quality "
            f"para {layer}.{table_name}: {messages}"
        )

    return results


def has_quality_failures(
    results: List[Dict]
) -> bool:
    """
    Retorna True se houver qualquer regra com status failed.
    """

    return any(
        result["status"] == "failed"
        for result in results
    )


def has_blocking_failures(
    results: List[Dict]
) -> bool:
    """
    Retorna True se houver falhas com severidade error.
    """

    return any(
        result["status"] == "failed"
        and result["severity"] == "error"
        for result in results
    )