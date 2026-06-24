"""
Configuração da API Dados Abertos da Câmara.

Centraliza os parâmetros usados nas requisições à API pública,
incluindo URL base, timeout, tentativas, paginação e identificação
do cliente.

As configurações podem ser carregadas a partir de variáveis de ambiente.
"""

API_CONFIG = {

    # =====================================================
    # BASE DA API 
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
    # PAGINAÇÃO
    # =====================================================

    "page_size": 50,

    "max_pages_per_execution": 100,

    # =====================================================
    # INGESTÃO DEPENDENTE
    # =====================================================

    "max_workers": 4,

    "max_parent_ids": 100,

    # =====================================================
    # CONTROLE DE LIMITE DE TAXA
    # =====================================================

    "request_sleep": 0.5,

    "nested_request_sleep": 0.2
}