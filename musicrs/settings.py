"""
MusicRS configurations
All configuration is read from .env file then pre-processed in settings.
"""
import os
import dotenv

dotenv.load_dotenv()

SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
