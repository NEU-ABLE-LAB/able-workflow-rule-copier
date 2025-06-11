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
        self, template_dir: Path, dest_dir: Path, cfg_path: Path
    ) -> None:  # noqa: D401
        self._dest_dir = dest_dir

    def copy(self, *, extra_answers: dict[str, Any]) -> _Result:  # noqa: D401
        inner = self._dest_dir / "copie0001"
        inner.mkdir(parents=True)
        (inner / "sentinel.txt").write_text("generated")
        return _Result(ok=True, project_dir=inner)


class _FailingCopie:
    """Simulates a Copier run that errored out."""

    def __init__(self, *a, **kw):  # noqa: D401, ANN001
        pass

    def copy(self, *, extra_answers: dict[str, Any]) -> _Result:  # noqa: D401
        return _Result(ok=False, project_dir=None, code=123)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_create_copier_config_creates_expected_artifacts(tmp_path: Path) -> None:
    cfg_path = seg._create_copier_config(tmp_path)

    #  paths exist
    assert cfg_path.is_file()
    assert (tmp_path / "copier").is_dir()
    assert (tmp_path / "copier_replay").is_dir()

    #  file isn’t empty and mentions both keys
    text = cfg_path.read_text()
    assert "copier_dir:" in text
    assert "replay_dir:" in text


def test_render_example_happy_path_flattens(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    #  Arrange sandbox to live entirely under tmp_path ────────────────────────
    monkeypatch.setattr(seg, "TEMPLATE_DIR", tmp_path / "template")
    monkeypatch.setattr(seg, "SANDBOX_ROOT", tmp_path / "sandbox")
    seg.TEMPLATE_DIR.mkdir()
    seg.SANDBOX_ROOT.mkdir()

    #  Minimal answers YAML
    answers_yml = tmp_path / "answers.yml"
    answers_yml.write_text("foo: bar\n")

    #  Patch Copie
    monkeypatch.setattr(seg, "Copie", _DummyCopie)

    #  Act
    seg._render_example(answers_yml)

    #  Assert – dest dir exists & was flattened
    dest = seg.SANDBOX_ROOT / answers_yml.stem
    assert dest.is_dir()
    assert (dest / "sentinel.txt").is_file()
    #  no leftover inner directory
    assert not any(dest.glob("copie000*"))


def test_render_example_raises_on_copy_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    answers_yml = tmp_path / "answers.yml"
    answers_yml.write_text("key: value\n")

    monkeypatch.setattr(seg, "TEMPLATE_DIR", tmp_path / "template")
    monkeypatch.setattr(seg, "SANDBOX_ROOT", tmp_path / "sandbox")
    seg.TEMPLATE_DIR.mkdir()
    seg.SANDBOX_ROOT.mkdir()
    monkeypatch.setattr(seg, "Copie", _FailingCopie)

    with pytest.raises(SystemExit) as excinfo:
        seg._render_example(answers_yml)

    assert excinfo.value.code == 123


def test_cli_generate_invokes_render(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    #  Prepare a fake answers file
    yml = tmp_path / "one.yml"
    yml.write_text("hello: 42\n")

    #  Capture calls to _render_example
    called: list[Path] = []

    def _fake_render_example(path: Path) -> None:  # noqa: D401
        called.append(path)

    monkeypatch.setattr(seg, "_render_example", _fake_render_example)

    #  Run CLI
    runner = CliRunner()
    result = runner.invoke(seg.app, ["generate", str(yml)])

    assert result.exit_code == 0
    assert Path(str(yml)) in called
