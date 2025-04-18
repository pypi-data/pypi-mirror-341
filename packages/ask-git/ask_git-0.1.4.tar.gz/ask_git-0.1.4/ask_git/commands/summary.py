import typer

from rich.console import Console
from rich.text import Text


from ask_git.git_utils.log import get_commits
from ask_git.prompt_builder import build_summary_prompt
from ask_git.ollama_client import send_to_ollama

from datetime import datetime

app = typer.Typer()
console = Console()

def print_summaries(commits: list[dict]):
    lines = []

    for c in commits:
        text = Text()
        text.append(f"🔧 Commit: ", style="bold cyan")
        text.append(c["sha"][:7] + "\n", style="bold white")

        text.append(f"👤 Author: ", style="bold green")
        text.append(c["author"] + "\n")

        text.append(f"📅 Date:   ", style="bold yellow")
        text.append(c["date"] + "\n")

        text.append(f"📝 Message: ", style="bold magenta")
        text.append(c["message"] + "\n")

        if c["files"]:
            text.append("📂 Files:\n", style="bold blue")
            for f in c["files"]:
                text.append(f"   • {f}\n", style="white")
        else:
            text.append("📂 Files: None\n", style="dim")

        # Separator
        text.append("\n" + "-" * 60 + "\n", style="dim")

        lines.append(text)

    # Show in scrollable pager
    with console.pager():
        for block in lines:
            console.print(block)


@app.command()
def main(
    since: str = typer.Option(None, help="Start date (e.g., '2024-01-01')"),
    until: str = typer.Option(
        default=datetime.today().strftime(r"%Y-%m-%d"), 
        help=(
            f"End date (e.g."
            f" {datetime.today().strftime(r"%Y-%m-%d")})"
            "(default: today)"
        )
    ),
    author: str = typer.Option(
        None,
        help="Filter commits by author name."
    ),
    max_count: int = typer.Option(
        None,
        help="Max number of commits to summarize."
    )
):
    """Summarize commits in a date range."""
    message = f"Summarizing commits"
    if since:
        message += f" from {since} - {until}"

    typer.echo(f"🔎 {message}")

    commit_objs = get_commits(
        since=since,
        until=until,
        author=author
    )

    if not commit_objs:
        typer.echo("⚠️ No commit messages found")
        return
    
    print_summaries(commit_objs)

    prompt = build_summary_prompt(commit_objs)
    typer.echo("\n🧠 Asking Codellama...\n")
    response = send_to_ollama(prompt=prompt)
    typer.echo(response)
    
    

