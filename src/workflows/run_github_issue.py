"""
GitHub Issue Runner mit Google Gemini Support
Liest ein GitHub Issue über die REST API aus, wandelt es in ein 
EngineeringTask-Modell um und führt die Agenten-Pipeline aus.
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
        title = issue_data.get("title", "No Title")
        body = issue_data.get("body", "No Description")
        
        description = f"GitHub Issue #{args.issue_number}: {title}\n\nTask Details / Description:\n{body}"
        print(f"\n--- Extracted Issue Content ---\n{description}\n-------------------------------\n")

        # 2. In das gemeinsame EngineeringTask Pydantic-Modell verpacken
        task = EngineeringTask(
            task_id=f"ISSUE-{args.issue_number}",
            description=description,
            input_files=["src/app/main.py"]
        )

        # 3. Die Feature Pipeline starten
        print("Starting Agentic Feature Pipeline Workflow...")
        result = run_feature_pipeline(task)
        
        print("\nPipeline execution completed successfully!")
        print(f"Result Status: {result.get('status')}")
        print(f"Trace & Evidence saved to evidence/session-02/")
        
    except Exception as exc:
        print(f"\nError executing pipeline for GitHub Issue: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
