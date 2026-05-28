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