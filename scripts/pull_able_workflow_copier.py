from __future__ import annotations

import subprocess
from pathlib import Path

from loguru import logger

REPO_URL = "https://github.com/NEU-ABLE-LAB/able-workflow-copier-dev.git"


def ensure_package_template_repo(project_root: Path) -> Path:
    """
    Guarantee that ``sandbox/able-workflow-copier-dev`` exists under *project_root*.
    If it is missing, do a shallow `git clone` and return the directory path.
    """
    dest = (project_root / "sandbox" / "able-workflow-copier-dev").resolve()
    if dest.is_dir():
        logger.debug("Package template already exists at {}", dest)
        return dest

    logger.debug("Cloning package template into {}", dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.check_call(["git", "clone", "--depth", "1", REPO_URL, str(dest)])
        logger.success("✔ cloned able-workflow-copier-dev → {}", dest)
    except FileNotFoundError:  # git not installed
        raise RuntimeError(
            "`git` executable not found - cannot clone package template."
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Git clone failed: {exc}") from exc

    return dest
