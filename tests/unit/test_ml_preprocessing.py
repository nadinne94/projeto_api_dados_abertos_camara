"""
Testes unitários do pré-processamento textual.

Valida a normalização de textos usados na classificação legislativa,
incluindo remoção de acentos, padronização de caixa, tratamento de espaços,
pontuação e valores nulos.
"""


import pytest

from src.ml.base.preprocessing import normalize_text


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Educação Pública", "educacao publica"),
        ("  Saúde!!!  ", "saude"),
        ("SEGURANÇA pública", "seguranca publica"),
        ("Meio-Ambiente", "meio ambiente"),
        ("", ""),
        (None, ""),
    ]
)
def test_normalize_text(input_text, expected):
    assert normalize_text(input_text) == expected