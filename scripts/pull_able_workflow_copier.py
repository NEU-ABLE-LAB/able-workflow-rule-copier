from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from loguru import logger
from ruamel.yaml import YAML

REPO_URL = "https://github.com/NEU-ABLE-LAB/able-workflow-copier-dev.git"
PR_YML_PATH = Path(__file__).parent.parent / ".github" / "workflows" / "pr.yml"


def get_commit_hash_from_pr_yml(pr_yml_path: Path) -> str:
    """
    Extract the commit hash from the `.github/workflows/pr.yml` file.
    """
    yaml = YAML(typ="safe")
    with pr_yml_path.open("r") as f:
        data: Any = yaml.load(f)
    try:
        steps = data["jobs"]["tox"]["steps"]
    except (KeyError, TypeError):
        raise RuntimeError("Could not find 'jobs.tox.steps' in pr.yml")
    for step in steps:
        if (
            isinstance(step, dict)
            and step.get("name", "").strip()
            == "Checkout the `able-workflow-copier` repository"
        ):
            ref = step.get("with", {}).get("ref")
            if isinstance(ref, str):
                return ref
            else:
                raise RuntimeError(
                    "Commit hash 'ref' not found or not a string in pr.yml"
                )
    raise RuntimeError("Could not find commit hash in pr.yml")


def ensure_package_template_repo(project_root: Path) -> Path:
    """
    Guarantee that ``sandbox/able-workflow-copier-dev`` exists under *project_root*.
    If it is missing, clone the repo, checkout the specific commit, and return the directory path.
    """
    dest = (project_root / "sandbox" / "able-workflow-copier-dev").resolve()
    if dest.is_dir():
        logger.debug("Package template already exists at {}", dest)
        return dest

    logger.debug("Cloning package template into {}", dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    commit_hash = get_commit_hash_from_pr_yml(PR_YML_PATH)
    try:
        subprocess.check_call(["git", "clone", REPO_URL, str(dest)])
        subprocess.check_call(["git", "config", "advice.detachedHead", "false"])
        subprocess.check_call(
            [
                "git",
                "-c",
                "advice.detachedHead=false",
                "checkout",
                commit_hash,
            ],
            cwd=str(dest),
        )
        logger.success(
            "✔ cloned able-workflow-copier-dev at commit {} → {}", commit_hash, dest
        )
    except FileNotFoundError:  # git not installed
        raise RuntimeError(
            "`git` executable not found - cannot clone package template."
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Git clone failed: {exc}") from exc

    return dest
