"""
Date time utilities
"""
from datetime import datetime


def timestamp_to_datetime(ts):
    """ Convert timestamp to datetime """
    return datetime.fromtimestamp(ts)


def datetime_to_timestamp(dt):
    """
    Convert datetime to timestamp
    param dt: datetime
    type dt: <class 'datetime.datetime'>
    """
    return datetime.timestamp(dt)
