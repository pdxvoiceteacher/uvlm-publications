import importlib


def test_atlas_api_server_import_smoke():
    mod = importlib.import_module("atlas.api_server")
    assert hasattr(mod, "app")
