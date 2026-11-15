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
        ("fixtures/HansePack_Katalog.json",),
        ("test_quotation.py",),
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
    project_id: str, target_dir: str | None
) -> None:
    """Ensure a run never targets the checkout of another project."""
    get_project(project_id)
    if target_dir is None:
        return
    target = Path(target_dir).resolve()
    for other in PROJECTS.values():
        if other.project_id == project_id:
            continue
        other_root = (REPO_ROOT / other.checkout_dir).resolve()
        if (
            target == other_root
            or target.is_relative_to(other_root)
            or other_root.is_relative_to(target)
            or target.name == other.checkout_dir
        ):
            raise ValueError(
                f"Project isolation violation: {project_id} must not target "
                f"{other.project_id} checkout {target}"
            )
