"""
Spark utilities.
"""

import logging

from pyspark.sql import SparkSession

from src.config.spark_config import SPARK_CONFIG

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """
    Configura níveis de logging.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        force=True
    )

    noisy_loggers = [

        "py4j",

        "py4j.clientserver",

        "urllib3",

        "pyspark",

        "delta"
    ]

    for name in noisy_loggers:

        logging.getLogger(
            name
        ).setLevel(
            logging.ERROR
        )


def get_spark(
    app_name: str = "camara_pipeline"
) -> SparkSession:
    """
    Retorna SparkSession configurada.
    """

    configure_logging()

    builder = (
        SparkSession.builder
        .appName(app_name)
    )

    for key, value in SPARK_CONFIG.items():

        builder = builder.config(
            key,
            value
        )

    spark = builder.getOrCreate()

    logger.info(
        "[SPARK] Session iniciada"
    )

    return spark


def set_spark_configs(
    spark: SparkSession
) -> None:
    """
    Aplica configurações Spark.
    """

    for key, value in SPARK_CONFIG.items():

        spark.conf.set(
            key,
            value
        )

    logger.info(
        "[SPARK] Configs aplicadas"
    )