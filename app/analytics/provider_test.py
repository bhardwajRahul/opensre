from __future__ import annotations

from pathlib import Path

from app.analytics import provider


def test_is_opted_out_in_ci_environment(monkeypatch) -> None:
    monkeypatch.setenv("CI", "true")

    assert provider._is_ci_environment() is True
    assert provider._is_opted_out() is True


def test_capture_first_run_if_needed_skips_files_in_ci(
    monkeypatch,
    tmp_path: Path,
) -> None:
    anonymous_id_path = tmp_path / "anonymous_id"
    first_run_path = tmp_path / "installed"

    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setattr(provider, "_ANONYMOUS_ID_PATH", anonymous_id_path)
    monkeypatch.setattr(provider, "_FIRST_RUN_PATH", first_run_path)
    monkeypatch.setattr(provider, "_CONFIG_DIR", tmp_path)
    monkeypatch.setattr(provider, "_instance", None)

    analytics = provider.Analytics()
    provider.capture_first_run_if_needed()

    assert analytics._disabled is True
    assert anonymous_id_path.exists() is False
    assert first_run_path.exists() is False
