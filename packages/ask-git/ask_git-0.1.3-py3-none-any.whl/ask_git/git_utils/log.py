from git import Repo
from datetime import datetime, timedelta
from typing import List, Dict, Optional

def get_commits(
    repo_path: str = ".", 
    max_count: Optional[int] = 20,
    since: Optional[str] = None,
    until: Optional[str] = None,
    author: Optional[str] = None,
) -> List[Dict]:
    repo = Repo(repo_path)
    commits = repo.iter_commits(max_count=max_count)

    # Convert since/until to datetime objects once
    since_dt = datetime.strptime(since, "%Y-%m-%d") if since else None
    until_dt = datetime.strptime(until, "%Y-%m-%d") + timedelta(days=1) if until else None

    results = []
    for c in commits:
        commit_date = datetime.fromtimestamp(c.committed_date)

        if since_dt and commit_date < since_dt:
            continue
        if until_dt and commit_date > until_dt:
            continue

        if author and author.lower() not in c.author.name.lower():
            continue

        files_changed = set()
        for diff_item in c.diff(c.parents[0] if c.parents else None):
            if diff_item.a_path:
                files_changed.add(diff_item.a_path)
            if diff_item.b_path:
                files_changed.add(diff_item.b_path)

        results.append({
            "sha": c.hexsha,
            "message": c.message.strip(),
            "author": c.author.name,
            "date": commit_date.strftime("%Y-%m-%d %H:%M"),
            "files": sorted(files_changed),
        })
    
    return results[:max_count]
