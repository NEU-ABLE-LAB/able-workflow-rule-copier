#!/usr/bin/env python3
"""
Render *extra-answers* YAML files into “sandbox examples” **without** pytest.

Each Example consists of two independent copier templates that will be applied
in a parent-then-child order:

1.  **Package** template  →  able-workflow-copier-dev
2.  **Rule**   template  →  this repository's root

For every example we

    1. create  sandbox/<example-name>/      (wiped if it already exists);
    2. run the *package* template there;
    3. reuse the output of (2) as the parent when we run the *rule* template;
    4. print the final project path so that you can open it in an editor.

Usage
-----

    # All examples
    python scripts/sandbox_examples_generate.py

    # Only specific examples
    python scripts/sandbox_examples_generate.py example-answers-able
"""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from pytest_copie.plugin import Copie, Result
from ruamel.yaml import YAML

###############################################################################
#  Convenience helpers                                                         #
###############################################################################


def _make_copier_config(work_root: Path) -> Path:
    """
    Re-implement the `_copier_config_file` fixture: create a copier config file
    that points into *work_root* and return its path.
    """
    copier_dir = work_root / "copier"
    replay_dir = work_root / "copier_replay"
    copier_dir.mkdir(parents=True, exist_ok=True)
    replay_dir.mkdir(parents=True, exist_ok=True)

    # Build a small copier-config and write it with ruamel.yaml
    config = {"copier_dir": str(copier_dir), "replay_dir": str(replay_dir)}
    config_path = work_root / "config"

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    with config_path.open("w", encoding="utf-8") as fp:
        yaml.dump(config, fp)

    return config_path


def _new_copie_instance(
    *,
    template_dir: Path,
    test_dir: Path,
    config_file: Path,
    parent_result: Result | None = None,
) -> Copie:
    """
    A tiny wrapper that makes it explicit what we need to pass to `Copie(...)`.
    """
    return Copie(
        default_template_dir=template_dir.resolve(),
        test_dir=test_dir.resolve(),
        config_file=config_file.resolve(),
        parent_result=parent_result,
    )


###############################################################################
#  Example definition                                                          #
###############################################################################


@dataclass
class Example:
    """Metadata for one sandbox rendering example."""

    name: str
    package_answers_file: Path
    rule_answers_file: Path
    package_answers: Dict[str, Any] | None = None
    rule_answers: Dict[str, Any] | None = None

    def __post_init__(self) -> None:
        yaml = YAML(typ="safe")
        self.package_answers = yaml.load(self.package_answers_file.read_text()) or {}
        self.rule_answers = yaml.load(self.rule_answers_file.read_text()) or {}


# ──────────────────────────────────────────────────────────────────────────────
#  Register all examples here
# ──────────────────────────────────────────────────────────────────────────────
EXAMPLES: List[Example] = [
    Example(
        name="example-answers-able",
        package_answers_file=Path("example-answers/weh_interviews/package.yml"),
        rule_answers_file=Path("example-answers/weh_interviews/rule.yml"),
    )
]

###############################################################################
#  Static paths used by every run                                              #
###############################################################################

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
TEMPLATE_PACKAGE_DIR: Path = PROJECT_ROOT / "../able-workflow-copier-dev"
TEMPLATE_RULE_DIR: Path = PROJECT_ROOT  # this repo
SANDBOX_ROOT: Path = PROJECT_ROOT / "sandbox"

###############################################################################
#  CLI                                                                         #
###############################################################################

app = typer.Typer(add_completion=False)  # we do not need shell completion


@app.command("generate")
def generate_cmd(
    examples: Optional[List[str]] = typer.Argument(
        None,
        help=(
            "Subset of examples to render "
            f"(available: {', '.join(e.name for e in EXAMPLES)})"
        ),
    )
) -> None:
    """
    Render one or more *extra-answers* files into the «sandbox» directory.

    The command works exactly the same way as the original pytest fixture would,
    but you can run it ad-hoc from the shell - no pytest needed.
    """
    SANDBOX_ROOT.mkdir(exist_ok=True)

    # Determine the list of examples we need to work on
    to_render: list[Example]
    if not examples:
        to_render = EXAMPLES
    else:
        lookup = {e.name: e for e in EXAMPLES}
        missing = [name for name in examples if name not in lookup]
        if missing:
            typer.echo(f"Unknown example name(s): {', '.join(missing)}", err=True)
            raise typer.Exit(1)
        to_render = [lookup[name] for name in examples]

    # Work each example
    for ex in to_render:
        ex_dir = SANDBOX_ROOT / ex.name
        if ex_dir.exists():
            shutil.rmtree(ex_dir)
        ex_dir.mkdir(parents=True)

        # A dedicated temp root for *all* Copie runs belonging to this example
        tmp_root = Path(tempfile.mkdtemp(prefix=f"copie_{ex.name}_"))
        config_file = _make_copier_config(tmp_root)

        # ───── 1. Run the *package* template ────────────────────────────────
        package_test_dir = ex_dir / "package_run"
        package_test_dir.mkdir()
        c_pkg = _new_copie_instance(
            template_dir=TEMPLATE_PACKAGE_DIR,
            test_dir=package_test_dir,
            config_file=config_file,
        )

        if ex.package_answers is None:  # pragma: no cover
            typer.echo(
                f"[{ex.name}] No package answers found, skipping package template.",
                err=True,
            )
            continue
        pkg_result = c_pkg.copy(extra_answers=ex.package_answers)

        if pkg_result.exception or pkg_result.exit_code != 0:  # pragma: no cover
            typer.echo(
                f"[{ex.name}] Package template failed: {pkg_result.exception}",
                err=True,
            )
            continue

        # ───── 2. Run the *rule* template (child) ───────────────────────────
        rule_test_dir = ex_dir / "rule_run"
        rule_test_dir.mkdir()
        c_rule = _new_copie_instance(
            template_dir=TEMPLATE_RULE_DIR,
            test_dir=rule_test_dir,
            config_file=config_file,
            parent_result=pkg_result,
        )
        if ex.rule_answers is None:
            typer.echo(
                f"[{ex.name}] No rule answers found, skipping rule template.",
                err=True,
            )
            continue
        rule_result = c_rule.copy(extra_answers=ex.rule_answers)

        if rule_result.exception or rule_result.exit_code != 0:  # pragma: no cover
            typer.echo(
                f"[{ex.name}] Rule template failed: {rule_result.exception}", err=True
            )
            continue

        typer.secho(
            f"[{ex.name}] ✔  Finished. Final project is at\n"
            f"    {rule_result.project_dir}",  # normally <sandbox>/<name>/rule_run/copie000/…
            fg="green",
        )

    typer.echo("All done.")


if __name__ == "__main__":
    app()
