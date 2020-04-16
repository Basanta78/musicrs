"""
Date time utilities
"""
from datetime import datetime


def timestamp_to_date(ts):
    """
    Convert timestamp to date.
    :param ts: timestamp
    :type ts: float
    """
    date = datetime.fromtimestamp(ts).date()
    return date.strftime("%Y-%m-%d")


def date_to_timestamp(date):
    """
    Convert date to timestamp.
    :param date: date (%Y-%m-%d) e.g 1970-01-01
    :type date: str
    """
    dt = datetime.strptime(date, "%Y-%m-%d")  # convert to datetime
    return datetime.timestamp(dt)
