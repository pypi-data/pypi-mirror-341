import click
import requests
import json

API_URL = "https://portal.k8or.com/chart/flow-4-portal-chart-cod-php-0427-rep-k8d-aws/v1/api/get-helm-chart"

@click.group()
def chart():
    """Helm chart commands."""
    pass

@chart.command("get")
@click.option("--image-uid", required=True, help="Image UID.")
@click.option("--image-version", required=True, help="Image version.")
def get_chart(image_uid, image_version):
    """Gets a Helm chart."""
    payload = {
        "imageUID": image_uid,
        "imageVersion": image_version,
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        click.echo(json.dumps(response.json(), indent=2))  # Print the formatted JSON response

    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}")
        if response is not None:
            click.echo(f"Response code was: {response.status_code}")
            try:
                click.echo(response.json())
            except json.JSONDecodeError:
                click.echo(response.text)
        else:
            click.echo("No response was provided.")