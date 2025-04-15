import click
import requests
import json

SCAN_API_URL = "https://portal.k8or.com/scan/flow-4-portal-scan-cod-php-0424-rep-k8d-aws/v1/api/scan-image"

@click.command("scan")
@click.option("--image-uid", required=True, help="Image UID.")
@click.option("--image-version", required=True, help="Image version.")
def scan_image(image_uid, image_version):
    """Scans an image for vulnerabilities."""
    payload = {
        "imageUID": image_uid,
        "imageVersion": image_version,
    }

    try:
        response = requests.post(SCAN_API_URL, json=payload)
        response.raise_for_status()  

        click.echo("Scan request sent successfully. Response:")
        click.echo(json.dumps(response.json(), indent=2)) 

    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}")
        if response is not None:
            click.echo(f"Response code: {response.status_code}")
            try:
                click.echo(json.dumps(response.json(), indent=2))
            except json.JSONDecodeError:
                click.echo(response.text) 
        else:
            click.echo("No response received from the server.")

if __name__ == '__main__':
    scan_image()

