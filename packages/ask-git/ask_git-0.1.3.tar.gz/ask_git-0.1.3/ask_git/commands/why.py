import typer

app = typer.Typer()

@app.command()
def main(
    file: str = typer.Argument(..., help="File to explain changes for")
):
    """Explain recent changes in a file."""
    typer.echo(f"Explaining recent changes in {file}")
