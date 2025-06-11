#!/usr/bin/env python3
"""
Render template “sandbox examples” from *extra-answers* YAML files.

The files listed in ``EXTRA_ANSWER_FILES`` contain **partial / overriding
answers** that supplement the defaults defined in the template’s
``copier.yml`` (or ``copier.yaml``).  They are **not** the
``.copier-answers.yml`` files created during an interactive run.

For each YAML file we:

1. Derive an output directory   →  ``sandbox/<stem>/``.
2. Clean that directory if it already exists.
3. Invoke ``copier copy`` with ``--defaults`` & ``--answers-file`` so
   the run is fully non-interactive.

Usage
-----
    python scripts/sandbox_examples_generate.py
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import typer
from pytest_copie.plugin import Copie
from ruamel.yaml import YAML


@dataclass
class Example:
    """Data structure for an example to render."""

    name: str
    package_answers: Path
    rule_answers: Path


EXAMPLES: List[Example] = [
    Example(
        name="example-answers-able",
        package_answers=Path("example-answers/weh_interviews/package.yml"),
        rule_answers=Path("example-answers/weh_interviews/rule.yml"),
    ),
]

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
# TODO-copier-rule: Pull the git repo of the project into the sandbox instead of assuming local copy exists.
TEMPLATE_PACKAGE_DIR: Path = PROJECT_ROOT / "../able-workflow-copier-dev"
TEMPLATE_RULE_DIR: Path = PROJECT_ROOT
SANDBOX_ROOT: Path = PROJECT_ROOT / "sandbox"


def _render_example(
    answers_yml: Path,
    template_dir: Path,
    dest_dir: Path,
    clean_dest: bool,
) -> None:
    """Run Copier once for ``answers_yml``.

    Parameters
    ----------
    answers_yml
        Extra-answers YAML file that overrides template defaults.
    """
    if not answers_yml.is_file():
        raise FileNotFoundError(f"Answers file not found: {answers_yml}")

    if dest_dir.exists() and clean_dest:
        shutil.rmtree(dest_dir)

    # --- 1. read answers YAML -> dict -----------------------------------------
    yaml = YAML(typ="safe")
    with answers_yml.open() as fp:
        answers_dict = yaml.load(fp) or {}

    # --- 2. build a minimal copier configuration ------------------------------
    copier_cfg = _create_copier_config(dest_dir / answers_yml.stem)

    # --- 3. run the copy through pytest-copie ---------------------------------
    copie = Copie(template_dir, dest_dir, copier_cfg)
    result = copie.copy(extra_answers=answers_dict)

    if result.exception:
        typer.echo(
            f"❌  Generating {answers_yml.name} failed "
            f"(exit={result.exit_code}): {result.exception}",
            err=True,
        )
        raise SystemExit(result.exit_code or 1)

    # pytest-copie nests the project inside dest_dir/copie000…  Flatten it.
    inner = result.project_dir
    if inner and inner.parent == dest_dir:
        for p in inner.iterdir():
            target = dest_dir / p.name
            if target.exists():
                shutil.rmtree(target) if target.is_dir() else target.unlink()
            p.rename(target)
        shutil.rmtree(inner, ignore_errors=True)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _create_copier_config(base: Path) -> Path:
    """Create the minimal config file expected by `Copie` and return its path."""
    copier_dir = base / "copier"
    replay_dir = base / "copier_replay"
    copier_dir.mkdir(parents=True, exist_ok=True)
    replay_dir.mkdir(exist_ok=True)

    cfg = {"copier_dir": str(copier_dir), "replay_dir": str(replay_dir)}
    cfg_path = base / "config"

    yaml = YAML(typ="safe")
    with cfg_path.open("w") as fp:
        yaml.dump(cfg, fp)

    return cfg_path


app = typer.Typer(help="Render sandbox examples from Copier extra-answer files.")


@app.command()
def generate(
    examples: Optional[List[str]] = typer.Argument(
        None,
        help=(
            "Name of examples to render." ", ".join([e.name for e in EXAMPLES])
            if EXAMPLES
            else "None"
        ),
    ),
) -> None:
    """
    Render each *extra-answers* YAML file into ``sandbox/<stem>/``.

    Examples
    --------

    # Render all defaults
    python scripts/sandbox_examples_generate.py

    # Render only a subset
    python scripts/sandbox_examples_generate.py example-answers-able.yml
    """
    SANDBOX_ROOT.mkdir(exist_ok=True)

    # Determine which examples to render
    examples_to_render: List[Example] = []
    if examples is None:
        examples_to_render = EXAMPLES
    else:
        for name in examples:
            example = next((e for e in EXAMPLES if e.name == name), None)
            if example is None:
                typer.echo(f"Example '{name}' not found.", err=True)
                raise typer.Exit(code=1)
            examples_to_render.append(example)

    # Render each example
    for example in examples_to_render:

        # Create the sandbox directory for this example
        example_dir = SANDBOX_ROOT / example.name
        example_dir.mkdir(exist_ok=True)

        # Render the package answers
        _render_example(
            answers_yml=example.package_answers,
            template_dir=TEMPLATE_PACKAGE_DIR,
            dest_dir=example_dir,
            clean_dest=True,
        )

        # Render the rule answers
        _render_example(
            answers_yml=example.rule_answers,
            template_dir=TEMPLATE_RULE_DIR,
            dest_dir=example_dir,
            clean_dest=False,
        )


if __name__ == "__main__":
    app()
