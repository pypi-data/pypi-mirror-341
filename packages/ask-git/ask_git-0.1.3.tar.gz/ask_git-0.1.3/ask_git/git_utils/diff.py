from git import Repo
from pathlib import Path

def get_diff_for_file(file_path: str, repo_path: str = ".") -> str:
    repo = Repo(repo_path)
    repo_root = Path(repo.working_tree_dir)
    full_path = Path(file_path).resolve()
    rel_path = full_path.relative_to(repo_root).as_posix()

    diffs = []

    # Unstaged diff (working tree vs index)
    try:
        unstaged = repo.git.diff(rel_path)
        if unstaged.strip():
            diffs.append("<<UNSTAGED CHANGES>>\n" + unstaged)
    except Exception as e:
        diffs.append(f"<<UNSTAGED DIFF ERROR>> {e}")

    # Staged diff (index vs HEAD)
    try:
        staged = repo.git.diff("--cached", rel_path)
        if staged.strip():
            diffs.append("<<STAGED CHANGES>>\n" + staged)
    except Exception as e:
        diffs.append(f"<<STAGED DIFF ERROR>> {e}")

    # Untracked
    if rel_path in repo.untracked_files:
        try:
            content = Path(file_path).read_text()
            diffs.append("<<UNTRACKED FILE>>\n" + content)
        except Exception as e:
            diffs.append(f"<<UNTRACKED FILE BUT CANNOT READ>> {e}")

    return "\n\n".join(diffs)
