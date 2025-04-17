import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def main(
    name: Annotated[str, typer.Argument(help="The name of the person to say goodbye to.")],
    template: Annotated[str, typer.Option("--template", "-t", help="The name of the template to use.")],
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

    print(f"Template: {template}")

if __name__ == "__main__":
    app()