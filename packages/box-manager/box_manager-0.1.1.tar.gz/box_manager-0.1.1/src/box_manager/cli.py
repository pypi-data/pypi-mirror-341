# box_manager/cli.py
import click
from box_manager import BoxManager

manager = BoxManager()

@click.group()
def cli():
    """BoxManager CLI"""
    pass

@click.command()
@click.argument('service')
def start(service):
    """Start a systemd service"""
    manager._run_systemctl('start', service)

@click.command()
@click.argument('service')
def stop(service):
    """Stop a systemd service"""
    manager._run_systemctl('stop', service)

@click.command()
@click.argument('service')
def status(service):
    """Check if a service is active"""
    is_active = manager.is_active(service)
    if is_active:
        click.echo(f"Service {service} is active.")
    else:
        click.echo(f"Service {service} is inactive.")

@click.command()
@click.argument('service')
def restart(service):
    """Restart a systemd service"""
    manager._run_systemctl('restart', service)

# Add the commands to the main CLI group
cli.add_command(start)
cli.add_command(stop)
cli.add_command(status)
cli.add_command(restart)

if __name__ == '__main__':
    cli()
