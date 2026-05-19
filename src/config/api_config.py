"""
API execution configuration.

Centraliza configurações de:
- requests HTTP
- retry / backoff
- paginação
- concorrência
- throttling
"""

API_CONFIG = {

    # =====================================================
    # API BASE
    # =====================================================

    "base_url":
        "https://dadosabertos.camara.leg.br/api/v2",

    # =====================================================
    # HTTP
    # =====================================================

    "timeout": 120,

    "max_retries": 8,

    "retry_delay": 2,

    # =====================================================
    # PAGINATION
    # =====================================================

    "page_size": 50,

    "max_pages_per_execution": 100,

    # =====================================================
    # NESTED INGESTION
    # =====================================================

    "max_workers": 4,

    "max_parent_ids": 100,

    # =====================================================
    # RATE LIMIT CONTROL
    # =====================================================

    "request_sleep": 0.5,

    "nested_request_sleep": 0.2
}