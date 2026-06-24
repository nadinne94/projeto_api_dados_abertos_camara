"""
Configuração da API Dados Abertos da Câmara.

Centraliza os parâmetros usados nas requisições à API pública,
incluindo URL base, timeout, tentativas, paginação e identificação
do cliente.

As configurações podem ser carregadas a partir de variáveis de ambiente.
"""

import os

from dotenv import load_dotenv


load_dotenv()


def _get_int_env(name: str, default: int) -> int:
    """Lê uma variável de ambiente inteira com fallback seguro."""

    value = os.getenv(name)

    if value in (None, ""):
        return default

    return int(value)


def _get_float_env(name: str, default: float) -> float:
    """Lê uma variável de ambiente float com fallback seguro."""

    value = os.getenv(name)

    if value in (None, ""):
        return default

    return float(value)


API_CONFIG = {
    # API BASE
    "base_url": os.getenv(
        "CAMARA_API_BASE_URL",
        "https://dadosabertos.camara.leg.br/api/v2",
    ),

    # HTTP
    "timeout": _get_int_env("CAMARA_API_TIMEOUT_SECONDS", 120),
    "max_retries": _get_int_env("CAMARA_API_MAX_RETRIES", 8),
    "retry_delay": _get_float_env("CAMARA_API_RETRY_SLEEP_SECONDS", 2.0),

    # PAGINAÇÃO
    "page_size": _get_int_env("CAMARA_API_PAGE_SIZE", 50),
    "max_pages_per_execution": _get_int_env(
        "CAMARA_API_MAX_PAGES_PER_EXECUTION",
        100,
    ),

    # INGESTÃO DEPENDENTE
    "max_workers": _get_int_env("CAMARA_API_MAX_WORKERS", 4),
    "max_parent_ids": _get_int_env("PIPELINE_MAX_PARENT_IDS", 100),

    # CONTROLE DE RATE LIMIT
    "request_sleep": _get_float_env("CAMARA_API_REQUEST_SLEEP_SECONDS", 0.5),
    "nested_request_sleep": _get_float_env(
        "CAMARA_API_NESTED_REQUEST_SLEEP_SECONDS",
        0.2,
    )
}