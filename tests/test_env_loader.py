import os

from app.env_loader import load_env


def test_load_env_sets_missing_and_never_overrides(tmp_path, monkeypatch):
    f = tmp_path / ".env"
    f.write_text("# comment\nALPHA_TEST=one\nexport BETA_TEST='two'\nGAMMA_TEST=\nKEEP_TEST=from_file\n", encoding="utf-8")
    for name in ("ALPHA_TEST", "BETA_TEST", "GAMMA_TEST"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("KEEP_TEST", "from_env")
    assert load_env(f) == 2
    assert os.environ["ALPHA_TEST"] == "one"
    assert os.environ["BETA_TEST"] == "two"
    assert "GAMMA_TEST" not in os.environ
    assert os.environ["KEEP_TEST"] == "from_env"
    for name in ("ALPHA_TEST", "BETA_TEST"):
        monkeypatch.delenv(name, raising=False)


def test_load_env_missing_file_is_noop(tmp_path):
    assert load_env(tmp_path / "nope.env") == 0