""" Logging utility module. """

import logging

from musicrs import config

logging.basicConfig(
    level=config["logging"]["level"], format=config["logging"]["format"]
)


def get_logger(name=None):
    """ Get logger instance. """
    return logging.getLogger(name)
