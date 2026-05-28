from src.ml.base.regex import find_regex_match


def test_find_regex_match_returns_expected_category():
    patterns = {
        "Saúde": [
            r"\bsaúde\b",
            r"\bsus\b"
        ],
        "Educação": [
            r"\beducação\b",
            r"\bescola\b"
        ],
    }

    result = find_regex_match(
        text="Projeto de lei sobre financiamento do SUS.",
        patterns=patterns
    )

    assert result == "Saúde"


def test_find_regex_match_returns_none_when_no_pattern_matches():
    patterns = {
        "Saúde": [
            r"\bsaúde\b",
            r"\bsus\b"
        ],
    }

    result = find_regex_match(
        text="Projeto sobre telecomunicações.",
        patterns=patterns
    )

    assert result is None