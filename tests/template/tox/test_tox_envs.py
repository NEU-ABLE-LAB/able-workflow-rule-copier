"""
Parametrise a test *dynamically* so that:

  - every answer-set (variant)          --> 'variant_id'
  - every tox env inside that variant   --> 'env_name'

gets its own, independent pytest test.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
import pytest

from loguru import logger

from tests.template.conftest import (
    EXAMPLES,
    _make_copier_config,
    _new_copie,
    TEMPLATE_PACKAGE_DIR,
    TEMPLATE_RULE_DIR,
)
from tests.template.tox.conftest import _list_tox_envs

###############################################################################
# 1.  Dynamic parametrisation --------------------------------------------------
###############################################################################


def pytest_generate_tests(metafunc):
    # Only apply to the test that asks for these args
    if {"variant_id", "env_name"} <= set(metafunc.fixturenames):

        argvalues: list[tuple[str, str]] = []
        argids: list[str] = []

        # Re-use / build a cache so we copy each variant only once
        cache: dict[str, tuple[Path, list[str]]] = getattr(
            metafunc.config, "_tox_collect_cache", {}
        )

        for ex in EXAMPLES:
            var_id = ex.name
            if var_id not in cache:
                #
                # ─── Render the example (package then rule) ─────────────────
                #
                tmp_root = Path(tempfile.mkdtemp(prefix=f"collect_{var_id}_"))
                config_file = _make_copier_config(tmp_root)

                # 1️⃣ package template
                pkg_dir = tmp_root / "pkg"
                pkg_dir.mkdir()
                pkg = _new_copie(
                    template_dir=TEMPLATE_PACKAGE_DIR,
                    test_dir=pkg_dir,
                    config_file=config_file,
                ).copy(extra_answers=ex.package_answers)

                # 2️⃣ rule template (child)
                rule_dir = tmp_root / "rule"
                rule_dir.mkdir()
                rule = _new_copie(
                    template_dir=TEMPLATE_RULE_DIR,
                    test_dir=rule_dir,
                    config_file=config_file,
                    parent_result=pkg,
                ).copy(extra_answers=ex.rule_answers)

                project_dir: Path = rule.project_dir
                envs = _list_tox_envs(project_dir)
                cache[var_id] = (project_dir, envs)

            project_dir, envs = cache[var_id]
            if not envs:
                logger.warning("No tox envs found for {}, skipping", var_id)
                continue

            for env in envs:
                argvalues.append((var_id, env))
                argids.append(f"{var_id}:{env}")

        metafunc.parametrize(
            ("variant_id", "env_name"), argvalues, ids=argids, scope="session"
        )
        metafunc.config._tox_collect_cache = cache

    else:
        logger.warning(f"Skipping dynamic param for {metafunc.function}")


###############################################################################
# 2.  The actual test ---------------------------------------------------------
###############################################################################


def test_inner_tox_env_passes(variant_id, env_name, request):
    """
    Re-use the already-rendered project captured during collection
    and assert that the selected tox environment exits cleanly.
    """
    project_dir, _ = request.config._tox_collect_cache[variant_id]

    completed = subprocess.run(
        ["tox", "run-parallel", "--parallel-no-spinner", "--quiet", "-e", env_name],
        cwd=project_dir,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (
        f"\n[variant = {variant_id!s}, env = {env_name!s}]\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}"
    )
