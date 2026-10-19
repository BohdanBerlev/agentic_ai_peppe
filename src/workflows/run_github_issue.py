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

    # 2. Optional: Ein Label 'in-progress' hinzufügen (falls im Repo vorhanden)
    label_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    httpx.post(label_url, headers=headers, json={"labels": ["in-progress"]})
