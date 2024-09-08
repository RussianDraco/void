"""
Functions to add:
install, uninstall, list, play, update, games, help


"""

import click

@click.group()
def cli():
    pass

@cli.command()
def ping():
    click.echo("pong")

