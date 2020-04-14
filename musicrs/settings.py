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
DATABASE_CONN = {
    "drivername": os.getenv("DRIVERNAME", "postgresql"),
    "host": os.getenv("HOST", "localhost"),
    "port": os.getenv("PORT", "5432"),
    "username": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DATABASE", "default"),
}
