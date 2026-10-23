"""
GitHub Issue Runner with strict Human Gate & status enforcement.
Does NOT auto-close issues when status is invalid_output, escalated, error,
changes_requested, or pending_human_review.
"""

import os
import sys
import argparse
from typing import Any
import httpx
from src.workflows.feature_pipeline import EngineeringTask, run_feature_pipeline


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
        error_msg = (
            f"⚠️ **Agentic Pipeline Eskalation / Fehler!**\n\n"
            f"- **Workflow-Status:** `{status}`\n"
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
    args = parser.parse_args()

    if not args.repo:
        print("Error: Repository not specified.")
        sys.exit(1)

    try:
        issue_data = fetch_issue_details(args.repo, args.issue_number)
        mark_issue_in_progress(args.repo, args.issue_number)

        title = issue_data.get("title", "No Title")
        body = issue_data.get("body", "No Description")
        description = f"GitHub Issue #{args.issue_number}: {title}\n\n{body}"

        task = EngineeringTask(
            task_id=f"ISSUE-{args.issue_number}",
            description=description,
            input_files=["src/app/main.py"],
        )

        print("Starting Agentic Feature Pipeline Workflow...")
        result = run_feature_pipeline(task)
        exit_code = handle_pipeline_result(args.repo, args.issue_number, result)
        sys.exit(exit_code)

    except Exception as exc:
        print(f"\nCRITICAL Error executing pipeline: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
