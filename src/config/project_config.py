"""
Global project configuration.

Centraliza paths de storage
da arquitetura medallion.
"""

# =========================================================
# BASE PATHS
# =========================================================

BASE_STORAGE_PATH = (
    "abfss://conteiner@"
    "arqmedallion.dfs.core.windows.net"
)

MEDALLION_PATH = (
    f"{BASE_STORAGE_PATH}/medallion"
)

ML_PATH = (
    f"{BASE_STORAGE_PATH}/ml"
)

METADATA_PATH = (
    f"{BASE_STORAGE_PATH}/metadata"
)

# =========================================================
# STORAGE CONFIGURATION
# =========================================================

STORAGE_CONFIG = {

    # MEDALLION

    "bronze":
        f"{MEDALLION_PATH}/bronze",

    "silver":
        f"{MEDALLION_PATH}/silver",

    "gold":
        f"{MEDALLION_PATH}/gold",

    # STAR SCHEMA

    "star":
        f"{MEDALLION_PATH}/gold/star_schema",

    # ML

    "ml_models":
        f"{ML_PATH}/models",

    # GOVERNANCE

    "logs":
        f"{METADATA_PATH}/logs",

    "watermark":
        f"{METADATA_PATH}/watermark"
}