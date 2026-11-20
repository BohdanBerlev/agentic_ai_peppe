"""Zentrale Projekt-Registry (Termin 6).

Ordnet einer project_id Kunde, Produkt-Checkout und Default-Eingaben/Tests zu.
Enthält außerdem den Guard, der verhindert, dass ein Lauf in den Checkout
eines anderen Projekts schreibt.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.agents.common import REPO_ROOT


@dataclass(frozen=True)
class ProjectConfig:
    project_id: str
    customer: str
    checkout_dir: str  # Ordnername des Produkt-Checkouts unter REPO_ROOT
    repository: str  # GitHub owner/name
    default_input_files: tuple[str, ...]
    default_test_targets: tuple[str, ...]
    default_issue_file: str | None = None


PROJECTS: dict[str, ProjectConfig] = {
    "client-01": ProjectConfig(
        "client-01",
        "Nordwerk Industrie-Service",
        "client-01-website",
        "DavidPisark/Nordwerk-Industrie-Service-Website",
        ("index.html",),
        ("test_website.py",),
    ),
    "client-02": ProjectConfig(
        "client-02",
        "HansePack",
        "client-02-quotation",
        "Vanitas50/client-02-quotation",
        ("quotation.py",),
        ("test_quotation.py",),
        default_issue_file="issue_hp01.md",
    ),
}


def get_project(project_id: str) -> ProjectConfig:
    """Return the ProjectConfig for project_id or raise ValueError."""
    try:
        return PROJECTS[project_id]
    except KeyError:
        raise ValueError(
            f"Unknown project_id: {project_id!r}. Known: {sorted(PROJECTS)}"
        ) from None


def default_checkout(project_id: str) -> Path:
    """Return the resolved checkout directory of a project."""
    return (REPO_ROOT / get_project(project_id).checkout_dir).resolve()


def assert_target_belongs_to_project(
    project_id: str, target_dir: str | Path | None
) -> None:
    """Ensure a run only writes to the positively assigned project area.

    Blocks foreign checkouts and all their subdirectories deterministically.
    """
    proj = get_project(project_id)
    if target_dir is None:
        return

    target = Path(target_dir).resolve()

    # 1. Negative Prüfung: Fremde Kundenbereiche (auch Unterverzeichnisse) strikt verbieten
    for other in PROJECTS.values():
        if other.project_id == project_id:
            continue
        other_root = (REPO_ROOT / other.checkout_dir).resolve()

        is_sub_of_other_root = False
        try:
            is_sub_of_other_root = (
                target == other_root
                or target.is_relative_to(other_root)
                or other_root.is_relative_to(target)
            )
        except ValueError:
            pass

        if (
            is_sub_of_other_root
            or any(part == other.checkout_dir or part == other.project_id for part in target.parts)
        ):
            raise ValueError(
                f"Project isolation violation: {project_id} must not target "
                f"{other.project_id} checkout or subdirectory: {target}"
            )

    # 2. Positive Prüfung: Begrenzung auf den positiv zugeordneten Projektbereich
    own_root = (REPO_ROOT / proj.checkout_dir).resolve()
    is_sub_of_own_root = False
    try:
        is_sub_of_own_root = target == own_root or target.is_relative_to(own_root)
    except ValueError:
        pass

    has_own_dir_marker = any(
        part == proj.checkout_dir or part == proj.project_id for part in target.parts
    )
    has_own_file_marker = False
    if target.is_dir():
        has_own_file_marker = any(
            (target / f).exists()
            for f in (proj.default_input_files + proj.default_test_targets)
        )

    in_own_scope = is_sub_of_own_root or has_own_dir_marker or has_own_file_marker
    if not in_own_scope:
        raise ValueError(
            f"Project isolation violation: target directory {target} is not in the "
            f"authorized scope for {project_id} ({proj.checkout_dir})"
        )
