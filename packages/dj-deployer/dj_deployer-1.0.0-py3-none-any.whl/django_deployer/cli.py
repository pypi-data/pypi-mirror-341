import click
import os
from .config import load_config, create_config_if_missing
from .deployer import deploy_project

@click.command()
@click.option('--config', default='deploy.yaml', help='Path to config file')
@click.option('--dry-run', is_flag=True, help='Preview commands without executing')
def main(config, dry_run):
    """📦 Deploy your Django project to a remote server via SSH."""
    if not os.path.exists(config):
        click.echo("🛠 No deploy.yaml found. Let's create one.")
        create_config_if_missing(config)

    conf = load_config(config)
    deploy_project(conf, dry_run=dry_run)
