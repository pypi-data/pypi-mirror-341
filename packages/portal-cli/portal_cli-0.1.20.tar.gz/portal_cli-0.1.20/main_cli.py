import click
from commands import upload, search, scan, chart, transfer, deploy, get_scan_data

# Define the version directly in this file
__version__ = "0.1.20"  # Change this to your desired version

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"portal-cli, version {__version__}")
    ctx.exit()

@click.group()
@click.option('--version', '-v', '--v', is_flag=True, expose_value=False, callback=print_version,
              help="Show version and exit")
def cli():
    """Multi-action CLI for image management."""
    pass

@cli.command('version')
def version_command():
    """Show the version of the CLI."""
    click.echo(f"portal-cli, version {__version__}")

cli.add_command(upload.upload)
cli.add_command(search.search)
cli.add_command(scan.scan)
cli.add_command(chart.chart)
cli.add_command(transfer.transfer)
cli.add_command(deploy.deploy)
cli.add_command(get_scan_data.get_scan_data)

if __name__ == "__main__":
    cli()

