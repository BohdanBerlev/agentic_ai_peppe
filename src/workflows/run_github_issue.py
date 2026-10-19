"""
GitHub Issue Runner mit detaillierter Fehleranalyse für Google Gemini.
"""

import os
import sys
import argparse
import httpx
from src.workflows.feature_pipeline import EngineeringTask, run_feature_pipeline

def fetch_issue_details(repo: str, issue_number: int) -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Environment variable GITHUB_TOKEN is missing.")
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
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
        "X-GitHub-Api-Version": "2022-11-28"
    }
    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    httpx.post(comment_url, headers=headers, json={"body": "🤖 **Agentic Pipeline gestartet!** Der Task wird bearbeitet (In Progress)."})
    
    label_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    httpx.post(label_url, headers=headers, json={"labels": ["in-progress"]})

def post_comment_only(repo: str, issue_number: int, message: str):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
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
        "X-GitHub-Api-Version": "2022-11-28"
    }
    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    httpx.post(comment_url, headers=headers, json={"body": f"🤖 **Pipeline erfolgreich!**\n\n{summary}"})
    
    patch_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    httpx.patch(patch_url, headers=headers, json={"state": "closed", "state_reason": "completed"})

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
            input_files=["src/app/main.py"]
        )

        print("Starting Agentic Feature Pipeline Workflow...")
        result = run_feature_pipeline(task)
        
        status = result.get('status', 'completed')
        print(f"\nPipeline finished with status: {status}")
        print(f"Full Result Object: {result}")

        if status in ['error', 'failed']:
            error_msg = f"⚠️ **Agentic Pipeline Fehler!**\n\nStatus: `{status}`.\nResult State: ```json\n{result}\n```"
            post_comment_only(args.repo, args.issue_number, error_msg)
            sys.exit(1)
        else:
            close_issue_with_success(args.repo, args.issue_number, f"Status: `{status}`. Traces saved.")
        
    except Exception as exc:
        print(f"\nCRITICAL Error executing pipeline: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
