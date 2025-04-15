import click
import subprocess  # Import the subprocess module
from commands import upload, search, scan, chart, transfer, deploy, get_scan_data

def get_version():
    """
    Gets the version from the setup.py file.
    """
    try:
        # Execute the python setup.py --version command and capture the output
        process = subprocess.run(
            ["python", "setup.py", "--version"],
            capture_output=True,
            text=True,  # Ensure output is returned as text
            check=True,  # Raise an exception for non-zero exit codes
        )
        version = process.stdout.strip()  # Remove leading/trailing whitespace
        return version
    except subprocess.CalledProcessError as e:
        # Handle errors, such as setup.py not existing or failing
        print(f"Error getting version from setup.py: {e}")
        return "Unknown"  # Return a default value or raise an exception
    except FileNotFoundError:
        print("Error: setup.py not found.  Make sure you are in the correct directory.")
        return "Unknown"

@click.group()
@click.version_option(version=get_version())  # Use the function to get the version
def cli():
    """Multi-action CLI for image management."""
    pass

cli.add_command(upload.upload)
cli.add_command(search.search)
cli.add_command(scan.scan)
cli.add_command(chart.chart)
cli.add_command(transfer.transfer)
cli.add_command(deploy.deploy)
cli.add_command(get_scan_data.get_scan_data)

if __name__ == "__main__":
    cli()

