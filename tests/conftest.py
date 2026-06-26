"""
Configuração compartilhada dos testes.

Centraliza fixtures reutilizáveis usadas pela suíte de testes, incluindo
a criação de uma SparkSession local para validação de transformações,
checks de qualidade e componentes auxiliares do projeto.
"""


import os
import sys

import pytest
from pyspark.sql import SparkSession


# ==========================================================
# Configuração do Python utilizado pelo PySpark
# ==========================================================

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT,
    )


@pytest.fixture(scope="session")
def spark():
    """
    Cria uma SparkSession local para testes unitários.

    A sessão é reaproveitada durante toda a suíte de testes.
    """

    spark_session = (
        SparkSession.builder
        .master("local[2]")
        .appName("projeto-camara-tests")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.sql.session.timeZone", "America/Sao_Paulo")
        .config("spark.pyspark.python", sys.executable)
        .config("spark.pyspark.driver.python", sys.executable)
        .getOrCreate()
    )

    yield spark_session

    spark_session.stop()