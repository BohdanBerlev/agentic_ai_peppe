"""
GitHub Issue Runner mit Google Gemini Support, In-Progress-Markierung und Auto-Close
Liest ein GitHub Issue über die REST API aus, führt die Agenten-Pipeline aus 
und aktualisiert den Status auf GitHub automatisch.
"""

import os
import sys
import argparse
import httpx
from src.workflows.feature_pipeline import EngineeringTask, run_feature_pipeline

def fetch_issue_details(repo: str, issue_number: int) -> dict:
    """Holt Titel und Beschreibung eines GitHub Issues über die GitHub REST API ab."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Environment variable GITHUB_TOKEN is missing.")
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    
    print(f"Fetching GitHub Issue #{issue_number} from repository '{repo}'...")
    response = httpx.get(url, headers=headers)
    
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch issue #{issue_number}: {response.status_code} - {response.text}")
    
    return response.json()

def mark_issue_in_progress(repo: str, issue_number: int):
    """Markiert das GitHub Issue als 'In Progress' via Kommentar und Label."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    # 1. Kommentar posten, dass die Agenten gestartet sind
    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    comment_payload = {
        "body": "🤖 **Agentic Pipeline gestartet!** Der Task wird nun von den Agenten bearbeitet und steht auf **In Progress**."
    }
    httpx.post(comment_url, headers=headers, json=comment_payload)

    # 2. Label 'in-progress' hinzufügen (hilft dem Project Board bei der Automatisierung)
    label_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    httpx.post(label_url, headers=headers, json={"labels": ["in-progress"]})

def close_issue_with_success(repo: str, issue_number: int, summary: str):
    """Postet einen Abschlusskommentar und schließt das GitHub Issue automatisch (Done)."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN not found, skipping auto-close.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    # 1. Kommentar mit dem Pipeline-Ergebnis posten
    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    comment_payload = {
        "body": f"🤖 **Agentic Pipeline Execution Successful!**\n\n{summary}\n\n*Status: Moved to Done automatically by Agent Runner.*"
    }
    
    print(f"Posting success comment to issue #{issue_number}...")
    comment_res = httpx.post(comment_url, headers=headers, json=comment_payload)
    if comment_res.status_code != 201:
        print(f"Warning: Could not post comment: {comment_res.status_code} - {comment_res.text}")

    # 2. Issue Status auf 'closed' (Done) setzen
    patch_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    patch_payload = {
        "state": "closed",
        "state_reason": "completed"
    }
    
    print(f"Closing GitHub Issue #{issue_number} (Done)...")
    patch_res = httpx.patch(patch_url, headers=headers, json=patch_payload)
    if patch_res.status_code == 200:
        print(f"Successfully closed issue #{issue_number}!")
    else:
        print(f"Warning: Could not close issue: {patch_res.status_code} - {patch_res.text}")

def main():
    parser = argparse.ArgumentParser(description="Run Agentic Feature Pipeline for a GitHub Issue via Gemini")
    parser.add_argument("--issue-number", type=int, required=True, help="The GitHub Issue number")
    parser.add_argument("--repo", type=str, default=os.getenv("GITHUB_REPOSITORY"), help="GitHub repository format owner/repo")
    args = parser.parse_args()

    if not args.repo:
        print("Error: Repository not specified and GITHUB_REPOSITORY environment variable is not set.")
        sys.exit(1)

    if not os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY") and not os.getenv("LLM_API_KEY"):
        print("Warning: API key for Gemini is not set in environment variables.")

    try:
        # 1. Issue von der GitHub REST API abrufen
        issue_data = fetch_issue_details(args.repo, args.issue_number)
        
        # 2. Direkt auf "In Progress" setzen (Kommentar & Label)
        mark_issue_in_progress(args.repo, args.issue_number)
        
        title = issue_data.get("title", "No Title")
        body = issue_data.get("body", "No Description")
        
        description = f"GitHub Issue #{args.issue_number}: {title}\n\nTask Details / Description:\n{body}"
        print(f"\n--- Extracted Issue Content ---\n{description}\n-------------------------------\n")

        # 3. In das gemeinsame EngineeringTask Pydantic-Modell verpacken
        task = EngineeringTask(
            task_id=f"ISSUE-{args.issue_number}",
            description=description,
            input_files=["src/app/main.py"]
        )

        # 4. Die Feature Pipeline starten
        print("Starting Agentic Feature Pipeline Workflow...")
        result = run_feature_pipeline(task)
        
        status = result.get('status', 'Completed')
        summary = f"Pipeline finished with status: `{status}`. Traces and evidence successfully saved locally."
        print(f"\nPipeline execution completed successfully!")

        # 5. Automatisches Schließen des Issues (Done) nach erfolgreichem Durchlauf
        close_issue_with_success(args.repo, args.issue_number, summary)
        
    except Exception as exc:
        print(f"\nError executing pipeline for GitHub Issue: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
