"""
Pytest configuration that mirrors the **parent → child** rendering
implemented in `scripts/sandbox_examples_generate.py`.

For each directory under `example-answers/<name>/` containing
  • `package.yml` - answers for the *package* template
  • `rule.yml`    - answers for the *rule*   template
we first render the package template (able-workflow-copier),
then render this repository's rule template with
``parent_result`` pointing to the package output.

The test fixture yields ``(project_dir, example_name)`` exactly like before.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, cast

import pytest
from loguru import logger
from ruamel.yaml import YAML

from pytest_copie.plugin import Copie

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
ensure_package_repo_path = PROJECT_ROOT / "scripts" / "pull_able_workflow_copier.py"
module_name = ensure_package_repo_path.stem
spec = importlib.util.spec_from_file_location(module_name, ensure_package_repo_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ensure_package_template_repo = module.ensure_package_template_repo


# ─────────────────────────────────────────────────────────────────────────────
# Static paths
# ─────────────────────────────────────────────────────────────────────────────


TEMPLATE_PACKAGE_DIR = ensure_package_template_repo(PROJECT_ROOT)
TEMPLATE_RULE_DIR = PROJECT_ROOT


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _make_copier_config(work_root: Path) -> Path:
    """Create a minimal copier-config file inside *work_root*."""
    copier_dir = work_root / "copier"
    replay_dir = work_root / "copier_replay"
    copier_dir.mkdir(parents=True, exist_ok=True)
    replay_dir.mkdir(parents=True, exist_ok=True)

    config_path = work_root / "config"
    YAML().dump(
        {"copier_dir": str(copier_dir), "replay_dir": str(replay_dir)},
        config_path.open("w", encoding="utf-8"),
    )
    return config_path


def _new_copie(
    *,
    template_dir: Path,
    test_dir: Path,
    config_file: Path,
    parent_result=None,
) -> Copie:  # type: ignore[name-defined]
    """Small wrapper around :class:`pytest_copie.plugin.Copie`."""
    return Copie(
        default_template_dir=template_dir.resolve(),
        test_dir=test_dir.resolve(),
        config_file=config_file.resolve(),
        parent_result=parent_result,
    )


def _run_copie_with_output_control(config, copie_session, answers):
    """Run copie_session.copy with output suppression based on pytest verbosity."""
    # Only suppress output if verbosity < 2 (i.e., not -vv or higher)
    if config.option.verbose < 2:
        with open(os.devnull, "w") as devnull:
            old_stdout, old_stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = devnull, devnull
            try:
                result = copie_session.copy(extra_answers=answers)
            finally:
                sys.stdout, sys.stderr = old_stdout, old_stderr
        return result
    else:
        # Run without output suppression for verbose modes
        return copie_session.copy(extra_answers=answers)


# ─────────────────────────────────────────────────────────────────────────────
# Example discovery
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class Example:
    name: str
    package_answers: Dict[str, Any]
    rule_answers: Dict[str, Any]


def _read_yaml(path: Path) -> Dict[str, Any]:
    return cast(Dict[str, Any], YAML(typ="safe").load(path.read_text()) or {})


def _discover_examples() -> List[Example]:
    examples: List[Example] = []
    for answers_dir in Path("example-answers").iterdir():
        if not answers_dir.is_dir():
            continue
        pkg = answers_dir / "package.yml"
        rule = answers_dir / "rule.yml"
        if pkg.exists() and rule.exists():
            examples.append(
                Example(
                    name=answers_dir.name,
                    package_answers=_read_yaml(pkg),
                    rule_answers=_read_yaml(rule),
                )
            )
    if not examples:
        raise RuntimeError(
            "No examples found under `example-answers/` - "
            "ensure each example has both `package.yml` and `rule.yml`."
        )
    return examples


EXAMPLES: List[Example] = _discover_examples()

# Nice parametrisation IDs
_example_ids = [ex.name for ex in EXAMPLES]


# ─────────────────────────────────────────────────────────────────────────────
# Fixture
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session", params=EXAMPLES, ids=_example_ids)
def rendered(request):
    """Render an example and yield (project_dir, example_name)."""
    example: Example = request.param

    tmp_root = Path(tempfile.mkdtemp(prefix=f"copie_{example.name}_"))
    config_file = _make_copier_config(tmp_root)

    # Package template (parent)
    pkg_dir = tmp_root / "package"
    pkg_dir.mkdir()
    pkg_copie = _new_copie(
        template_dir=TEMPLATE_PACKAGE_DIR,
        test_dir=pkg_dir,
        config_file=config_file,
    )

    # Run the package template with output control
    # to avoid cluttering the test output with copier's own logs.
    # This is especially useful when running tests with `-v` or `-vv`.
    pkg_result = _run_copie_with_output_control(
        request.config, pkg_copie, example.package_answers
    )

    # Smoke test the package template
    if pkg_result.exit_code or pkg_result.exception:
        pytest.fail(
            f"Package template failed for {example.name}: {pkg_result.exception}"
        )

    # Rule template (child)
    rule_dir = tmp_root / "rule"
    rule_dir.mkdir()
    rule_copie = _new_copie(
        template_dir=TEMPLATE_RULE_DIR,
        test_dir=rule_dir,
        config_file=config_file,
        parent_result=pkg_result,
    )

    # Run the rule template with output control
    # to avoid cluttering the test output with copier's own logs.
    # This is especially useful when running tests with `-v` or `-vv`.
    rule_result = _run_copie_with_output_control(
        request.config, rule_copie, example.rule_answers
    )

    # Smoke test the rule template
    if rule_result.exit_code or rule_result.exception:
        pytest.fail(f"Rule template failed for {example.name}: {rule_result.exception}")

    logger.debug(f"Rendered '{example.name}' → {rule_result.project_dir}")
    return rule_result.project_dir, example.name
