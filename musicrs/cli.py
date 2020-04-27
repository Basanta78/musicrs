""" Musicrs click command"""
import click
from musicrs.util.db import reset_db
from musicrs.recommendation_engine.inference import load_inference


@click.group(invoke_without_command=False)
def main():
    pass


@main.command()
def reset():
    reset_db()


@main.command()
@click.option("--file-path", required=True)
def inference(file_path):
    load_inference(file_path)
