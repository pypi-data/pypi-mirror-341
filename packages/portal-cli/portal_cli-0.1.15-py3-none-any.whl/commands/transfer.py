import click

@click.group()
def transfer():
    """Image transfer commands."""
    pass

@transfer.command("to-registry")
@click.option("--image", required=True, help="Image to transfer.")
@click.option("--registry", required=True, help="Target registry.")
def transfer_to_registry(image, registry):
    """Transfers an image to a registry."""
    click.echo(f"Transferring {image} to {registry}")