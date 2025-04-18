from git import Repo

def get_blame_for_file(file_path: str, repo_path: str = "."):
    repo = Repo(repo_path)
    return repo.blame("HEAD", file_path)
