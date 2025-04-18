from git import Repo
from pathlib import Path
from typing import List, Dict


def is_git_repo(path=".") -> bool:
    """
    Check if the given path is a Git repository.

    Args:
        path (str): Path to check (default is current directory).

    Returns:
        bool: True if the path is a Git repo, False otherwise.
    """
    return (Path(path) / ".git").exists()


def get_commit_metadata(repo_path: str = ".", max_count: int = 10) -> List[Dict]:
    """
    Retrieve metadata for the latest commits in the repository.

    Args:
        repo_path (str): Path to the Git repository.
        max_count (int): Number of recent commits to return.

    Returns:
        List[Dict]: List of dictionaries with commit hash, author, email, date, and message.
    """
    repo = Repo(repo_path)
    metadata = []
    for commit in repo.iter_commits(max_count=max_count):
        metadata.append({
            "hash": commit.hexsha[:7],
            "author": commit.author.name,
            "email": commit.author.email,
            "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M"),
            "message": commit.message.strip()
        })
    return metadata


def get_changes_between_commits(commit1: str, commit2: str, repo_path: str = ".") -> str:
    """
    Get the diff between two commits.

    Args:
        commit1 (str): The older commit hash or reference.
        commit2 (str): The newer commit hash or reference.
        repo_path (str): Path to the Git repository.

    Returns:
        str: The raw diff output between the two commits.
    """
    repo = Repo(repo_path)
    return repo.git.diff(commit1, commit2)


def get_repo_root(path: Path = Path.cwd()) -> Path:
    """
    Get the root directory of the Git repository.

    Args:
        path (Path): Any path inside the repo.

    Returns:
        Path: Path to the root of the Git repository.
    """
    return Path(Repo(path, search_parent_directories=True).working_dir)

def get_relative_path_from_repo_root(file_path: Path) -> str:
    """
    Convert absolute file path to repo-relative path.

    Args:
        file_path (Path): Absolute or relative file path.

    Returns:
        str: Path relative to the root of the Git repository.
    """
    repo_root = get_repo_root()
    return str(file_path.resolve().relative_to(repo_root))

