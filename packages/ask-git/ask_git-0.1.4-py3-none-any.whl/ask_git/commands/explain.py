import typer

from pathlib import Path

from rich.console import Console
from rich.text import Text

from ask_git.git_utils.diff import get_diff_for_file
from ask_git.git_utils.blame import get_blame_for_file
from ask_git.git_utils.utils import get_relative_path_from_repo_root

from ask_git.prompt_builder import build_explain_prompt

from ask_git.ollama_client import send_to_ollama   

app = typer.Typer()
console = Console(height=8)

def print_colored_diff(diff: str):
    styled_text = Text()

    for line in diff.splitlines():
        if line in ["<<UNSTAGED CHANGES>>", "<<STAGED CHANGES>>", "<<UNTRACKED FILE>>"]:
            styled_text.append(line + "\n", style="bold blue on white")
        elif line.startswith("+") and not line.startswith("+++"):
            styled_text.append(line + "\n", style="green")
        elif line.startswith("-") and not line.startswith("---"):
            styled_text.append(line + "\n", style="red")
        else:
            styled_text.append(line + "\n")

    with console.pager(styles=True):
        console.print(styled_text)


@app.command()
def main(
    file: str = typer.Argument(..., help="File to analyze"),
    line_start: int = typer.Option(None, help="Optional start line number"),
    line_end: int = typer.Option(None, help="Optional end line number")
):
    """Explain why a file or a range of lines changed."""
    path = Path(file).resolve()
    if not path.exists():
        typer.echo(f"❌ File path '{path}' does not exist!")
        raise typer.Exit()

    # Print analysis context message
    message = f"🔍 Analyzing changes in: {path}"
    if line_end and not line_start:
        typer.echo("❌ Line end given but no line start.")
        raise typer.Exit()
    elif line_start and not line_end:
        message += f" (starting from line {line_start})"
    elif line_start and line_end:
        message += f" (lines {line_start} to {line_end})"
    typer.echo(message)

    # Get relative path to repo root for GitPython diff
    relative_path = get_relative_path_from_repo_root(path)

    # Get full diff for the file
    diff = get_diff_for_file(str(relative_path))
    if not diff:
        typer.echo("⚠️ No diffs found for this file.")
        return

    # Show the full diff (line range slicing skipped)
    typer.echo(
        f"\n📄 Git Diff (full file shown, selected lines "
        f"{line_start}-{line_end or line_start}):\n"
    )

    print_colored_diff(diff)

    # Show blame output if line_start is provided
    blame_lines = []
    if line_start:
        blame = get_blame_for_file(str(path))
        typer.echo(f"\n📌 Blame for lines {line_start} to {line_end or line_start}:\n")

        current_line = 1
        found = False

        for commit, lines in blame:
            for line in lines:
                if line_start <= current_line <= (line_end or line_start):
                    typer.echo(
                        f"• Line {current_line} by "
                        f"{commit.author.name}: {line.strip()}"
                    )
                    blame_lines.append(
                        (current_line, commit.author.name, line.strip())
                    )                   
                    found = True
                current_line += 1

        if not found:
            typer.echo("⚠️ No matching lines found in blame output.")
    
    prompt = build_explain_prompt(
        file=str(path),
        line_start=line_start,
        line_end=(line_end or line_start),
        diff=diff,
        blame_lines=blame_lines
    )
    typer.echo("\n🧠 Asking Codellama...\n")
    response = send_to_ollama(prompt)
    typer.echo(response)


