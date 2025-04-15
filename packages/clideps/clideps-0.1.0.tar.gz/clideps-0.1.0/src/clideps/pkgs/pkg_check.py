from __future__ import annotations

import logging
import shutil
from pathlib import Path

from prettyfmt import fmt_path

from clideps.pkgs.pkg_checker_registry import run_checker
from clideps.pkgs.pkg_info import get_all_common_pkgs, get_pkg
from clideps.pkgs.pkg_model import (
    CheckInfo,
    DepType,
    Pkg,
    PkgCheckResult,
    PkgDep,
    PkgInfo,
    PkgName,
)

log = logging.getLogger(__name__)


def which_tool(pkg: PkgInfo) -> tuple[Path | None, CheckInfo]:
    """
    Does one of the package's commands exist in the path?
    This only works for packages that have installed commands (not pure
    libraries).
    """
    found_path = next(filter(None, (shutil.which(name) for name in pkg.command_names)), None)
    path = Path(found_path) if found_path else None
    return (
        path,
        f"Found `{path.name}` at `{fmt_path(path)}`"
        if path
        else f"Did not find in path: {', '.join(pkg.command_names)}",
    )


def pkg_check(
    mandatory: list[PkgName] | None = None,
    recommended: list[PkgName] | None = None,
    optional: list[PkgName] | None = None,
) -> PkgCheckResult:
    """
    Main function to check which dependencies are installed. Validates the given
    package names. The usual list is mandatory dependencies, but recommended
    and optional dependencies can also be listed.

    If no dependencies are listed, all known dependencies will be checked as
    optional dependencies.
    """
    if not mandatory and not recommended and not optional:
        optional = [pkg.name for pkg in get_all_common_pkgs()]

    found_pkgs: list[Pkg] = []
    missing_required: list[Pkg] = []
    missing_recommended: list[Pkg] = []
    missing_optional: list[Pkg] = []
    found_info: dict[PkgName, CheckInfo] = {}
    missing_info: dict[PkgName, CheckInfo] = {}

    # Check names and assemble dependencies.
    deps: list[PkgDep] = []
    for pkg_name_str in mandatory or []:
        pkg = get_pkg(pkg_name_str)
        deps.append(PkgDep(pkg_name_str, pkg.info, DepType.mandatory))
    for pkg_name_str in recommended or []:
        pkg = get_pkg(pkg_name_str)
        deps.append(PkgDep(pkg_name_str, pkg.info, DepType.recommended))
    for pkg_name_str in optional or []:
        pkg = get_pkg(pkg_name_str)
        deps.append(PkgDep(pkg_name_str, pkg.info, DepType.optional))

    for dep in deps:
        # First check if the tools are in the path.
        which_path, which_info = which_tool(dep.pkg_info)
        if which_path:
            success, check_info = True, which_info
        else:
            # Otherwise use a checker function.
            # Ensure common checkers are imported.
            import clideps.pkgs.common_pkg_checkers  # pyright: ignore  # noqa: F401

            success, check_info = run_checker(dep.pkg_name)
            log.info(f"Checker result for {dep.pkg_name}: {success} {check_info}")
        if success:
            found_info[dep.pkg_name] = check_info
            found_pkgs.append(dep.pkg)
        else:
            missing_info[dep.pkg_name] = check_info
            if dep.dep_type == DepType.mandatory:
                missing_required.append(dep.pkg)
            elif dep.dep_type == DepType.recommended:
                missing_recommended.append(dep.pkg)
            else:
                missing_optional.append(dep.pkg)

    found_pkgs.sort()
    missing_required.sort()
    missing_recommended.sort()
    missing_optional.sort()

    return PkgCheckResult(
        found_pkgs,
        missing_required,
        missing_recommended,
        missing_optional,
        found_info,
        missing_info,
    )


def warn_if_missing(pkg_names: list[PkgName]) -> list[PkgName]:
    """
    Warn if the given packages are not installed.
    """
    result = pkg_check(pkg_names)
    return result.warn_if_missing(*pkg_names)
