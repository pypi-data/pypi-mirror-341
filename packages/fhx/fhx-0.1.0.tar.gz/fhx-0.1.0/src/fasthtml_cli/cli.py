import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def main(
    name: Annotated[str, typer.Argument(help="The name of the person to say goodbye to.")],
    reload: Annotated[bool, typer.Option("--reload", "-r", help="Enable live  reload.")] = False,
    formal: Annotated[bool, typer.Option(help="Whether to say goodbye formally.")] = False
    ):
    """
    Say goodbye to someone.
    """
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")
    
    if reload:
        print("Reloading...")
    else:
        print("Not reloading...")

if __name__ == "__main__":
    app()