"""
Configuração global do projeto.

Centraliza os caminhos de armazenamento da arquitetura lakehouse.
As configurações podem ser carregadas a partir de variáveis de ambiente.
"""

import os

from dotenv import load_dotenv


load_dotenv()

# =========================================================
# CAMINHOS DE ARMAZENAMENTO
# =========================================================

BASE_STORAGE_PATH = os.getenv(
    "BASE_STORAGE_PATH",
    "file:/tmp/dados_abertos_camara",
)

MEDALLION_PATH = os.getenv(
    "MEDALLION_PATH",
    f"{BASE_STORAGE_PATH}/medallion",
)

ML_PATH = os.getenv(
    "ML_PATH",
    f"{BASE_STORAGE_PATH}/ml",
)

METADATA_PATH = os.getenv(
    "METADATA_PATH",
    f"{BASE_STORAGE_PATH}/metadata",
)

# =========================================================
# CONFIGURAÇÕES DE ARMAZENAMENTO
# =========================================================

STORAGE_CONFIG: dict[str, str] = {
    # ARQUITETURA MEDALLION
    "bronze": os.getenv(
        "BRONZE_PATH",
        f"{MEDALLION_PATH}/bronze",
    ),
    "silver": os.getenv(
        "SILVER_PATH",
        f"{MEDALLION_PATH}/silver",
    ),
    "gold": os.getenv(
        "GOLD_PATH",
        f"{MEDALLION_PATH}/gold",
    ),

    # STAR SCHEMA
    "star": os.getenv(
        "STAR_PATH",
        f"{MEDALLION_PATH}/gold/star_schema",
    ),

    # ML
    "ml_models": os.getenv(
        "ML_MODELS_PATH",
        f"{ML_PATH}/models",
    ),

    # GOVERNANÇA
    "logs": os.getenv(
        "LOGS_PATH",
        f"{METADATA_PATH}/logs",
    ),
    "watermark": os.getenv(
        "WATERMARK_PATH",
        f"{METADATA_PATH}/watermark",
    )
}