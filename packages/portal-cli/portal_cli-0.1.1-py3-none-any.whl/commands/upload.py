import click

@click.group()
def upload():
    """Image upload commands."""
    pass

@upload.command("image")
@click.option("--image", required=True, help="Path to the image file.")
def upload_image(image):
    """Uploads a Docker image."""
    click.echo(f"Uploading image: {image}")