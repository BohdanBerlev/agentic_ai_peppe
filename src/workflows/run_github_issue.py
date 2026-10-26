"""
GitHub Issue Runner with strict Human Gate & status enforcement.
Does NOT auto-close issues when status is invalid_output, escalated, error,
changes_requested, or pending_human_review.
"""

import argparse
import os
import sys
from typing import Any

import httpx

from src.app.settings import get_settings
from src.workflows.feature_pipeline import EngineeringTask, run_feature_pipeline


def extract_intended_actor(body: str) -> str | None:
    """Read the 'Intended actor' value from a GitHub issue-form body."""
    if not body:
        return None
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if "intended actor" in line.lower():
            for nxt in lines[i + 1 :]:
                value = nxt.strip()
                if not value or value.startswith("#"):
                    continue
                return value
    return None


def fetch_issue_details(repo: str, issue_number: int) -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Environment variable GITHUB_TOKEN is missing.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    response = httpx.get(url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch issue #{issue_number}: {response.status_code} - {response.text}")

    return response.json()


def mark_issue_in_progress(repo: str, issue_number: int):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    httpx.post(
        comment_url,
        headers=headers,
        json={"body": "🤖 **Agentic Pipeline gestartet!** Der Task wird bearbeitet (In Progress)."},
    )

    label_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    httpx.post(label_url, headers=headers, json={"labels": ["in-progress"]})


def post_comment_only(repo: str, issue_number: int, message: str):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    httpx.post(comment_url, headers=headers, json={"body": message})


def close_issue_with_success(repo: str, issue_number: int, summary: str):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    httpx.post(
        comment_url,
        headers=headers,
        json={"body": f"🤖 **Pipeline abgeschlossen & menschlich freigegeben!**\n\n{summary}"},
    )

    patch_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    httpx.patch(patch_url, headers=headers, json={"state": "closed", "state_reason": "completed"})


def should_close_issue(result: dict[str, Any]) -> bool:
    """Only close an issue if the workflow succeeded AND an accountable human explicitly approved it."""
    status = result.get("status")
    if status != "success":
        return False
    approval = result.get("result_state", {}).get("human_approval", {})
    decision = approval.get("decision")
    reviewed_by = approval.get("reviewed_by")
    return decision == "approved" and bool(reviewed_by)


def handle_pipeline_result(repo: str, issue_number: int, result: dict[str, Any]) -> int:
    """Process pipeline outcome: close only on verified human approval; keep open otherwise."""
    status = result.get("status", "error")
    approval = result.get("result_state", {}).get("human_approval", {})
    decision = approval.get("decision", "escalate_to_human_review")
    recommendation = approval.get("agent_recommendation", "unknown")
    reviewed_by = approval.get("reviewed_by")

    if status in ("error", "failed", "invalid_output", "escalated"):
        pipeline_error = result.get("result_state", {}).get("pipeline_error") or result.get("error")
        error_details = f"- **Fehler:** `{pipeline_error}`\n" if pipeline_error else ""
        print(f"\n❌ Pipeline-Fehler aufgetreten:\nStatus: {status}\n{error_details}", flush=True)
        error_msg = (
            f"⚠️ **Agentic Pipeline Eskalation / Fehler!**\n\n"
            f"- **Workflow-Status:** `{status}`\n"
            f"{error_details}"
            f"- **Gate-Entscheidung:** `{decision}`\n"
            f"- **Hinweis:** Issue bleibt offen zur menschlichen Prüfung.\n"
        )
        post_comment_only(repo, issue_number, error_msg)
        return 1

    if should_close_issue(result):
        close_issue_with_success(
            repo,
            issue_number,
            f"Status: `{status}` | Human Approval: `{decision}` durch **{reviewed_by}**.",
        )
        return 0

    # Pipeline ran cleanly, but decision is pending_human_review or changes_requested
    msg = (
        f"🛑 **Human Gate erforderlich / Nachbesserung nötig** (Issue bleibt offen)\n\n"
        f"- **Workflow-Status:** `{status}`\n"
        f"- **Agenten-Empfehlung:** `{recommendation}`\n"
        f"- **Human-Gate-Status:** `{decision}` (Reviewer: `{reviewed_by or 'ausstehend'}`)\n"
        f"- **Notiz:** {approval.get('note', '-')}"
    )
    post_comment_only(repo, issue_number, msg)
    return 0 if decision == "pending_human_review" else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--repo", type=str, default=os.getenv("GITHUB_REPOSITORY"))
    parser.add_argument("--target-dir", type=str, default=os.getenv("TARGET_DIR", None))
    parser.add_argument("--project-id", type=str, default=os.getenv("PROJECT_ID", "client-01"))
    args = parser.parse_args()

    if not args.repo:
        print("Error: Repository not specified.")
        sys.exit(1)

    try:
        issue_data = fetch_issue_details(args.repo, args.issue_number)

        actor = extract_intended_actor(issue_data.get("body") or "")
        if actor and actor.lower() != "agent":
            post_comment_only(
                args.repo,
                args.issue_number,
                f"⏭️ **Übersprungen** – Intended actor: `{actor}`. "
                "Die Agentic Pipeline läuft nur für Issues mit Intended actor = **Agent**.",
            )
            print(f"Skipping issue #{args.issue_number}: intended actor is '{actor}'.")
            sys.exit(0)

        mark_issue_in_progress(args.repo, args.issue_number)

        settings = get_settings()
        api_key_found = bool(
            settings.llm_api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or os.getenv("LLM_API_KEY")
            or os.getenv("AI_STUDIO_API_KEY")
        )
        print(f"🔧 Pre-flight check: Provider={settings.llm_provider}, Model={settings.llm_model}, API-Key vorhanden={api_key_found}")
        if settings.llm_provider == "google" and not api_key_found:
            raise RuntimeError(
                "Kein Google AI Studio API-Key konfiguriert! Bitte stelle sicher, dass unter Repository Settings -> Secrets and variables -> Actions "
                "ein Secret namens GEMINI_API_KEY oder GOOGLE_API_KEY hinterlegt ist."
            )

        title = issue_data.get("title", "No Title")
        body = issue_data.get("body", "No Description")
        description = f"GitHub Issue #{args.issue_number}: {title}\n\n{body}"

        input_files = ["index.html"] if args.target_dir else ["src/app/main.py"]
        test_targets = ["test_website.py"] if args.target_dir else ["tests/test_work_items_api.py"]

        task = EngineeringTask(
            task_id=f"ISSUE-{args.issue_number}",
            description=description,
            project_id=args.project_id,
            target_dir=args.target_dir,
            input_files=input_files,
            test_targets=test_targets,
        )

        print("Starting Agentic Feature Pipeline Workflow...")
        result = run_feature_pipeline(task)
        exit_code = handle_pipeline_result(args.repo, args.issue_number, result)
        sys.exit(exit_code)

    except Exception as exc:
        print(f"\nCRITICAL Error executing pipeline: {exc}")
        try:
            if args.repo and args.issue_number:
                error_body = (
                    f"❌ **Fehler bei der Ausführung der Agentic Pipeline:**\n\n"
                    f"```text\n{exc}\n```\n\n"
                    f"**Hinweise zur Fehlerbehebung:**\n"
                    f"- Prüfe, ob in den GitHub Repository Secrets (`Settings -> Secrets and variables -> Actions`) "
                    f"das Secret `GEMINI_API_KEY` oder `GOOGLE_API_KEY` angelegt ist.\n"
                    f"- Stelle sicher, dass der Key in Google AI Studio aktiv und gültig ist.\n"
                    f"- Detaillierte Laufzeitlogs findest du im Tab **Actions** dieses Repositories."
                )
                post_comment_only(args.repo, args.issue_number, error_body)
        except Exception as post_err:
            print(f"Failed to post failure comment to issue: {post_err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
