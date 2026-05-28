"""
Checks reutilizáveis de Data Quality para DataFrames Spark.

As funções deste módulo retornam dicionários padronizados com o resultado
da validação, em vez de interromperem diretamente a execução.

A decisão de falhar ou apenas registrar warning fica concentrada no
runner de qualidade.
"""

from typing import Iterable, Optional

from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def _result(
    rule_name: str,
    status: str,
    severity: str,
    message: str,
    metric_value=None,
    expected_value=None
) -> dict:
    """
    Cria uma resposta padronizada para uma regra de Data Quality.
    """

    return {
        "rule_name": rule_name,
        "status": status,
        "severity": severity,
        "message": message,
        "metric_value": metric_value,
        "expected_value": expected_value
    }


def check_not_empty(
    df: DataFrame,
    severity: str = "error"
) -> dict:
    """
    Valida se o DataFrame possui pelo menos um registro.
    """

    has_rows = df.limit(1).count() > 0

    if has_rows:
        return _result(
            rule_name="not_empty",
            status="passed",
            severity=severity,
            message="DataFrame possui registros.",
            metric_value=True,
            expected_value=True
        )

    return _result(
        rule_name="not_empty",
        status="failed",
        severity=severity,
        message="DataFrame está vazio.",
        metric_value=False,
        expected_value=True
    )


def check_required_columns(
    df: DataFrame,
    required_columns: Iterable[str],
    severity: str = "error"
) -> dict:
    """
    Valida se todas as colunas obrigatórias existem no DataFrame.
    """

    required_columns = list(required_columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if not missing_columns:
        return _result(
            rule_name="required_columns",
            status="passed",
            severity=severity,
            message="Todas as colunas obrigatórias estão presentes.",
            metric_value=[],
            expected_value=required_columns
        )

    return _result(
        rule_name="required_columns",
        status="failed",
        severity=severity,
        message=f"Colunas obrigatórias ausentes: {missing_columns}",
        metric_value=missing_columns,
        expected_value=required_columns
    )


def check_no_nulls(
    df: DataFrame,
    columns: Iterable[str],
    severity: str = "error"
) -> dict:
    """
    Valida se as colunas informadas não possuem valores nulos.
    """

    columns = list(columns)

    missing_columns = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing_columns:
        return _result(
            rule_name="no_nulls",
            status="failed",
            severity=severity,
            message=f"Colunas não encontradas para validação de nulos: {missing_columns}",
            metric_value=missing_columns,
            expected_value=columns
        )

    columns_with_nulls = []

    for column in columns:
        has_null = (
            df
            .filter(col(column).isNull())
            .limit(1)
            .count()
            > 0
        )

        if has_null:
            columns_with_nulls.append(column)

    if not columns_with_nulls:
        return _result(
            rule_name="no_nulls",
            status="passed",
            severity=severity,
            message="Colunas validadas não possuem nulos.",
            metric_value=[],
            expected_value=columns
        )

    return _result(
        rule_name="no_nulls",
        status="failed",
        severity=severity,
        message=f"Colunas com valores nulos: {columns_with_nulls}",
        metric_value=columns_with_nulls,
        expected_value=columns
    )


def check_unique_key(
    df: DataFrame,
    key_columns: Iterable[str],
    severity: str = "error"
) -> dict:
    """
    Valida se a combinação de colunas informada é única.
    """

    key_columns = list(key_columns)

    missing_columns = [
        column
        for column in key_columns
        if column not in df.columns
    ]

    if missing_columns:
        return _result(
            rule_name="unique_key",
            status="failed",
            severity=severity,
            message=f"Colunas de chave não encontradas: {missing_columns}",
            metric_value=missing_columns,
            expected_value=key_columns
        )

    duplicated_count = (
        df
        .groupBy(*key_columns)
        .count()
        .filter(col("count") > 1)
        .limit(1)
        .count()
    )

    if duplicated_count == 0:
        return _result(
            rule_name="unique_key",
            status="passed",
            severity=severity,
            message=f"Chave {key_columns} é única.",
            metric_value=0,
            expected_value=0
        )

    return _result(
        rule_name="unique_key",
        status="failed",
        severity=severity,
        message=f"Foram encontradas duplicidades na chave {key_columns}.",
        metric_value=duplicated_count,
        expected_value=0
    )


def check_max_null_ratio(
    df: DataFrame,
    column_name: str,
    max_ratio: float,
    severity: str = "warning"
) -> dict:
    """
    Valida se a proporção de nulos de uma coluna está abaixo do limite.
    """

    if column_name not in df.columns:
        return _result(
            rule_name="max_null_ratio",
            status="failed",
            severity=severity,
            message=f"Coluna não encontrada: {column_name}",
            metric_value=None,
            expected_value=max_ratio
        )

    total_rows = df.count()

    if total_rows == 0:
        return _result(
            rule_name="max_null_ratio",
            status="failed",
            severity=severity,
            message="DataFrame vazio. Não é possível calcular proporção de nulos.",
            metric_value=None,
            expected_value=max_ratio
        )

    null_rows = (
        df
        .filter(col(column_name).isNull())
        .count()
    )

    null_ratio = null_rows / total_rows

    if null_ratio <= max_ratio:
        return _result(
            rule_name="max_null_ratio",
            status="passed",
            severity=severity,
            message=(
                f"Proporção de nulos da coluna '{column_name}' dentro do limite."
            ),
            metric_value=null_ratio,
            expected_value=max_ratio
        )

    return _result(
        rule_name="max_null_ratio",
        status="failed",
        severity=severity,
        message=(
            f"Proporção de nulos da coluna '{column_name}' acima do limite."
        ),
        metric_value=null_ratio,
        expected_value=max_ratio
    )


def check_allowed_values(
    df: DataFrame,
    column_name: str,
    allowed_values: Iterable,
    severity: str = "error"
) -> dict:
    """
    Valida se uma coluna possui apenas valores dentro de um domínio permitido.
    """

    allowed_values = list(allowed_values)

    if column_name not in df.columns:
        return _result(
            rule_name="allowed_values",
            status="failed",
            severity=severity,
            message=f"Coluna não encontrada: {column_name}",
            metric_value=None,
            expected_value=allowed_values
        )

    invalid_count = (
        df
        .filter(
            col(column_name).isNotNull()
            & ~col(column_name).isin(allowed_values)
        )
        .limit(1)
        .count()
    )

    if invalid_count == 0:
        return _result(
            rule_name="allowed_values",
            status="passed",
            severity=severity,
            message=f"Coluna '{column_name}' contém apenas valores permitidos.",
            metric_value=0,
            expected_value=allowed_values
        )

    return _result(
        rule_name="allowed_values",
        status="failed",
        severity=severity,
        message=f"Coluna '{column_name}' possui valores fora do domínio permitido.",
        metric_value=invalid_count,
        expected_value=allowed_values
    )


def check_min_rows(
    df: DataFrame,
    min_rows: int,
    severity: str = "error"
) -> dict:
    """
    Valida se o DataFrame possui quantidade mínima de registros.
    """

    row_count = df.count()

    if row_count >= min_rows:
        return _result(
            rule_name="min_rows",
            status="passed",
            severity=severity,
            message="Quantidade de registros atende ao mínimo esperado.",
            metric_value=row_count,
            expected_value=min_rows
        )

    return _result(
        rule_name="min_rows",
        status="failed",
        severity=severity,
        message="Quantidade de registros abaixo do mínimo esperado.",
        metric_value=row_count,
        expected_value=min_rows
    )


def check_value_range(
    df: DataFrame,
    column_name: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    severity: str = "error"
) -> dict:
    """
    Valida se os valores de uma coluna estão dentro de um intervalo.
    """

    if column_name not in df.columns:
        return _result(
            rule_name="value_range",
            status="failed",
            severity=severity,
            message=f"Coluna não encontrada: {column_name}",
            metric_value=None,
            expected_value={
                "min_value": min_value,
                "max_value": max_value
            }
        )

    condition = col(column_name).isNotNull()

    if min_value is not None:
        condition = condition & (col(column_name) < min_value)

    if max_value is not None:
        condition = condition | (
            col(column_name).isNotNull()
            & (col(column_name) > max_value)
        )

    invalid_count = (
        df
        .filter(condition)
        .limit(1)
        .count()
    )

    if invalid_count == 0:
        return _result(
            rule_name="value_range",
            status="passed",
            severity=severity,
            message=f"Coluna '{column_name}' está dentro do intervalo esperado.",
            metric_value=0,
            expected_value={
                "min_value": min_value,
                "max_value": max_value
            }
        )

    return _result(
        rule_name="value_range",
        status="failed",
        severity=severity,
        message=f"Coluna '{column_name}' possui valores fora do intervalo esperado.",
        metric_value=invalid_count,
        expected_value={
            "min_value": min_value,
            "max_value": max_value
        }
    )