"""
Incremental watermark manager.
"""

import logging

from typing import Optional

from delta.tables import DeltaTable

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

from pyspark.sql.functions import max as spark_max

from pyspark.sql.types import (
    StructField,
    StructType,
    StringType,
)

logger = logging.getLogger(__name__)


class WatermarkManager:

    """
    Gerencia watermarks incrementais.
    """

    def __init__(
        self,
        spark: SparkSession,
        watermark_path: str
    ):

        self.spark = spark

        self.watermark_path = (
            watermark_path
        )

        self.schema = StructType([

            StructField(
                "dataset",
                StringType(),
                True
            ),

            StructField(
                "last_value",
                StringType(),
                True
            )
        ])

    def get_watermark(
        self,
        dataset: str
    ) -> Optional[str]:
        """
        Retorna watermark atual.
        """

        try:

            if not DeltaTable.isDeltaTable(
                self.spark,
                self.watermark_path
            ):

                return None

            df = (
                self.spark.read
                .format("delta")
                .load(
                    self.watermark_path
                )
            )

            row = (

                df
                .filter(
                    df.dataset == dataset
                )
                .first()
            )

            if row is None:

                return None

            return row["last_value"]

        except Exception as exc:

            logger.warning(
                "[WATERMARK] get failed: %s",
                exc
            )

            return None

    def update_watermark(
        self,
        dataset: str,
        value: str
    ) -> None:
        """
        Atualiza watermark.
        """

        logger.info(
            "[WATERMARK] update %s=%s",
            dataset,
            value
        )

        data = [{

            "dataset": dataset,

            "last_value": value
        }]

        df = self.spark.createDataFrame(
            data,
            schema=self.schema
        )

        if not DeltaTable.isDeltaTable(
            self.spark,
            self.watermark_path
        ):

            (
                df.write
                .format("delta")
                .mode("overwrite")
                .save(
                    self.watermark_path
                )
            )

            return

        delta_table = DeltaTable.forPath(
            self.spark,
            self.watermark_path
        )

        update_map = {

            column:
            f"source.{column}"

            for column in df.columns
        }

        (
            delta_table.alias("target")
            .merge(
                df.alias("source"),
                """
                target.dataset =
                source.dataset
                """
            )
            .whenMatchedUpdate(
                set=update_map
            )
            .whenNotMatchedInsert(
                values=update_map
            )
            .execute()
        )

    def apply_incremental_params(
        self,
        dataset_name: str,
        config: dict,
        params: dict
    ) -> dict:
        """
        Aplica parâmetros incrementais.
        """

        if not config.get(
            "incremental"
        ):

            return params

        incremental_param = config.get(
            "incremental_param"
        )

        if not incremental_param:

            return params

        watermark = self.get_watermark(
            dataset_name
        )

        if watermark:

            params[
                incremental_param
            ] = watermark

            logger.info(
                "[WATERMARK] %s >= %s",
                incremental_param,
                watermark
            )

        return params

    def update_incremental_watermark(
        self,
        dataset_name: str,
        config: dict,
        df: DataFrame
    ) -> None:
        """
        Atualiza watermark pós ingestão.
        """

        if not config.get(
            "incremental"
        ):

            return

        incremental_field = config.get(
            "incremental_field"
        )

        if incremental_field not in df.columns:

            return

        max_value = (

            df
            .agg(
                spark_max(
                    incremental_field
                )
            )
            .first()[0]
        )

        if max_value is None:

            return

        self.update_watermark(

            dataset_name,

            str(max_value)[:10]
        )