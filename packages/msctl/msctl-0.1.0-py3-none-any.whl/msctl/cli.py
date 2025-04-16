import click
from msctl.commands import manager_cmd

@click.group()
@click.version_option()
def cli():
    """Microservices Manager CLI."""
    pass

# Register commands
cli.add_command(manager_cmd.hello)
if __name__ == '__main__':
    cli()