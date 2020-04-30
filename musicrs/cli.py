""" Musicrs click command"""
import click
from datetime import timedelta, date
from musicrs.util.db import reset_db
from musicrs.recommendation_engine.inference import load_inference
from musicrs.recommendation_engine.recommend import recommend_music
from musicrs.recommendation_engine.user_profile import load_slack_messages


@click.group(invoke_without_command=False)
def main():
    pass


@main.command()
def reset():
    reset_db()


@main.command()
@click.option("--file-path", "-p", required=True)
def inference(file_path):
    load_inference(file_path)


@main.command()
@click.option(
    "--start-date", "-s", required=False, default=date.today() - timedelta(days=10)
)
@click.option("--end-date", "-e", required=False, default=date.today())
def message(start_date, end_date):
    load_slack_messages(start_date, end_date)


@main.command()
@click.option("--user-id", "-u", required=True)
def recommend(user_id):
    recommend_music(user_id)
