import click

@click.group()
def deploy():
    """Image deployment commands."""
    pass

@deploy.command("image")
@click.option("--image", required=True, help="Image to deploy.")
@click.option("--namespace", default="default", help="Namespace to deploy to.")
def deploy_image(image, namespace):
    """Deploys an image to a Kubernetes cluster."""
    click.echo(f"Deploying {image} to {namespace}")