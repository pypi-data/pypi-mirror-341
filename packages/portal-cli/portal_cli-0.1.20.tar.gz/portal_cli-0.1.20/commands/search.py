import click

@click.group()
def search():
    """Image search commands."""
    pass

@search.command("by-name")
@click.option("--name", required=True, help="Image name to search for.")
def search_by_name(name):
    """Searches for images by name."""
    click.echo(f"Searching for image: {name}")