""" Database connection API. """

import pyodbc

from musicrs.util.object import merge
from musicrs.util.db import build_connstr

from musicrs.api.logging import get_logger

logger = get_logger("musicrs.api.db")


def connect(**params) -> pyodbc.Connection:
    """ Open connection to a Database. """
    logger.debug(
        "Connecting to database: {}/{}".format(
            params.get("host"), params.get("database")
        )
    )

    connstr = build_connstr(**params)

    return pyodbc.connect(connstr)
