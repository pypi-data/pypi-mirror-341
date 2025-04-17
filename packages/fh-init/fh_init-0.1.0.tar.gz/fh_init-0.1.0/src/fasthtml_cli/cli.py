import typer
from typing_extensions import Annotated
from fasthtml_cli.fasthtml_templates.basic import basic

app = typer.Typer()

templates = ["basic", "minimal", "tailwind"]

@app.command()
def main(
    name: Annotated[str, typer.Argument(help="The name of the person to say goodbye to.")],
    template: Annotated[str, typer.Option("--template", "-t", help="The name of the template to use.")] =  "base",
    reload: Annotated[bool, typer.Option("--reload", "-r", help="Enable live reload.")] = False,
    uv: Annotated[bool, typer.Option(help="Use uv to manage project dependencies.")] = True
    ):
    """
    Say goodbye to someone.
    """
    if uv:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")
    
    if reload:
        print("Reloading...")
    else:
        print("Not reloading...")

    # whitelist template
    if template not in templates:
        template = templates[0]

    print(f"Template: {template}")

    if template == "basic":
        basic_template = basic()
        print(basic_template)

if __name__ == "__main__":
    app()