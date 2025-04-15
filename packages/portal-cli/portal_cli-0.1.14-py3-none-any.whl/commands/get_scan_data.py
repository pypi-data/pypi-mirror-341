import click
import requests
import json

SCAN_DATA_API_URL = "https://portal.k8or.com/scan/flow-4-portal-scan-cod-php-0424-rep-k8d-aws/v1/api/get-scan-data"

@click.command("get-scan-data")
@click.option("--image-uid", required=True, help="Image UID.")
@click.option("--image-version", required=True, help="Image version.")
def get_scan_data(image_uid, image_version):
    """Retrieves previously scanned data for a given image."""
    payload = {
        "imageUID": image_uid,
        "imageVersion": image_version,
    }

    try:
        response = requests.post(SCAN_DATA_API_URL, json=payload)
        response.raise_for_status() 

        click.echo("Successfully retrieved scan data. Response:")
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
    get_scan_data()

