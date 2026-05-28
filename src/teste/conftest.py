import os
import sys

import pytest
from pyspark.sql import SparkSession


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT
    )


@pytest.fixture(scope="session")
def spark():
    """
    Cria uma SparkSession local para testes unitários.

    A sessão é reaproveitada durante toda a suíte de testes.
    """

    spark_session = (
        SparkSession
        .builder
        .master("local[2]")
        .appName("projeto-camara-tests")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )

    yield spark_session

    spark_session.stop()