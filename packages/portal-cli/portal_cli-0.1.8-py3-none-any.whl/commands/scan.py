import click

@click.group()
def scan():
    """Image scan commands."""
    pass

@scan.command("vulnerabilities")
@click.option("--image", required=True, help="Image to scan for vulnerabilities.")
def scan_vulnerabilities(image):
    """Scans an image for vulnerabilities."""
    click.echo(f"Scanning image: {image}")