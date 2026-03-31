from __future__ import annotations

from pathlib import Path

from loguru import logger

PARENT_TEMPLATE_SUBMODULE = Path("submodules") / "able-workflow-copier"


def _missing_submodule_error(project_root: Path, submodule_dir: Path) -> RuntimeError:
    return RuntimeError(
        "Required parent template submodule is missing or not initialized.\n"
        f"Expected path: {submodule_dir}\n"
        "Initialize submodules from the repository root with:\n"
        "  git submodule update --init --recursive\n"
        f"Repository root: {project_root}"
    )


def ensure_package_template_repo(project_root: Path) -> Path:
    """
    Return the path to the checked-out parent template submodule.

    The caller is expected to initialize git submodules before running tests.
    This helper fails fast with actionable guidance when the submodule is missing.
    """
    dest = (project_root / PARENT_TEMPLATE_SUBMODULE).resolve()
    if not dest.is_dir():
        raise _missing_submodule_error(project_root, dest)
    if not (dest / ".git").exists():
        raise _missing_submodule_error(project_root, dest)

    logger.debug("Using parent template submodule at {}", dest)

    return dest
