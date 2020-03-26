import os

from logging import INFO, DEBUG, ERROR, WARNING, CRITICAL


name = "musicrs"
version = "0.0.12-alpha.20200319130820"

log_level_map = {
    "info": INFO,
    "debug": DEBUG,
    "error": ERROR,
    "warning": WARNING,
    "critical": CRITICAL,
}

# TODO: Decide later where would be the best way to put the config.
config: object = {
    # Logging configurationsF
    "logging": {
        "level": log_level_map.get(os.getenv("LOG_LEVEL", "debug")),
        "format": "%(asctime)s - [ %(levelname)s ] %(name)s - %(message)s",
    },
    # AWS configuration credentials
    "aws": {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    },
}
