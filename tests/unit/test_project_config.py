from src.config.project_config import STORAGE_CONFIG


def test_storage_config_has_required_keys():
    expected_keys = {
        "bronze",
        "silver",
        "gold",
        "star",
        "ml_models",
        "logs",
        "watermark",
    }

    assert expected_keys.issubset(STORAGE_CONFIG.keys())


def test_storage_config_paths_are_not_empty():
    for path in STORAGE_CONFIG.values():
        assert path is not None
        assert isinstance(path, str)
        assert len(path) > 0


def test_star_path_points_to_gold_star_schema():
    assert STORAGE_CONFIG["star"].endswith("/medallion/gold/star_schema")