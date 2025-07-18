"""
Unit tests for `scripts/sandbox_examples_generate.py`.

These tests avoid running Copier for real by monkey-patching the
`Copie` class with light stubs.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

# ---------------------------------------------------------------------------
# Dynamically import the script under test (scripts/ isn’t a Python package)
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]  # project root (…/repo/)
SCRIPT_PATH = ROOT_DIR / "scripts" / "sandbox_examples_generate.py"

spec = importlib.util.spec_from_file_location("sandbox_examples_generate", SCRIPT_PATH)
seg = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
sys.modules["sandbox_examples_generate"] = seg  # let patches work across tests
assert spec.loader  # mypy: for None-guard
spec.loader.exec_module(seg)  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Helpers – lightweight stubs that stand in for pytest-copie
# ---------------------------------------------------------------------------
class _Result:
    """Mimics the object returned by `Copie.copy()` in pytest-copie."""

    def __init__(
        self, *, ok: bool = True, project_dir: Path | None = None, code: int = 0
    ):
        self.exception: Exception | None = None if ok else RuntimeError("copy failed")
        self.exit_code = 0 if ok else code
        self.project_dir = project_dir


class _DummyCopie:
    """Successful copy that creates an inner directory the code will flatten."""

    def __init__(
        self,
        default_template_dir: Path,
        test_dir: Path,
        config_file: Path,
        parent_result: _Result | None = None,
    ):
        self._dest_dir = test_dir

    def copy(self, *, extra_answers: dict[str, Any]) -> _Result:  # noqa: D401
        inner = self._dest_dir / "copie000"
        inner.mkdir(parents=True)
        (inner / "sentinel.txt").write_text("generated")
        return _Result(ok=True, project_dir=inner)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_make_copier_config_creates_expected_artifacts(tmp_path: Path) -> None:
    """_make_copier_config should write a proper YAML file + dirs."""
    cfg_path = seg._make_copier_config(tmp_path)

    #  paths exist
    assert cfg_path.is_file()
    assert (tmp_path / "copier").is_dir()
    assert (tmp_path / "copier_replay").is_dir()

    #  file isn’t empty and mentions both keys
    text = cfg_path.read_text()
    assert "copier_dir:" in text
    assert "replay_dir:" in text


def _prepare_single_example(
    tmp_path: Path,
    *,
    monkeypatch: pytest.MonkeyPatch,
) -> (Any, Any):
    """Return ``(sentinel_path, example_name)`` for the synthetic example."""
    # 1. minimal YAML files expected by Example dataclass --------------------
    pkg_yml = tmp_path / "pkg.yml"
    rule_yml = tmp_path / "rule.yml"
    pkg_yml.write_text("a: 1\n")
    rule_yml.write_text("b: 2\n")

    example = seg.Example(
        name="fake-example",
        package_answers_file=pkg_yml,
        rule_answers_file=rule_yml,
    )

    # 2. patch EXAMPLES to contain *only* our synthetic entry ----------------
    monkeypatch.setattr(seg, "EXAMPLES", [example])

    # 3. make sandbox + template dirs under tmp_path -------------------------
    monkeypatch.setattr(seg, "SANDBOX_ROOT", tmp_path / "sandbox")
    monkeypatch.setattr(seg, "TEMPLATE_PACKAGE_DIR", tmp_path / "tpl_pkg")
    monkeypatch.setattr(seg, "TEMPLATE_RULE_DIR", tmp_path / "tpl_rule")
    seg.SANDBOX_ROOT.mkdir()
    seg.TEMPLATE_PACKAGE_DIR.mkdir()
    seg.TEMPLATE_RULE_DIR.mkdir()

    # 4. stub Copie ----------------------------------------------------------
    monkeypatch.setattr(seg, "Copie", _DummyCopie)

    # The script’s logic will end up here:
    sentinel = (
        seg.SANDBOX_ROOT
        / f"example-{example.name}"
        / "rule_run"
        / "copie000"
        / "sentinel.txt"
    )
    return sentinel, example.name


def test_cli_generate_happy_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CLI renders the sandbox and leaves our sentinel file in place."""
    sentinel, ex_name = _prepare_single_example(tmp_path, monkeypatch=monkeypatch)

    runner = CliRunner()
    # pass the example name so the command exits cleanly (exit-code 0)
    result = runner.invoke(seg.app, ["fake-example", ex_name])

    assert result.exit_code == 0
    assert sentinel.is_file()
