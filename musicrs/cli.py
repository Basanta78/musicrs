""" Musicrs click command"""
import click
from musicrs.util.db import reset_db


@click.group(invoke_without_command=False)
def main():
    pass


@main.command()
def reset():
    reset_db()
