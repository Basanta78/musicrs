""" Database utility module. """

import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from musicrs.model.base import Base
from musicrs.settings import DATABASE_CONN


def create_db_engine():
    """ Create database connection engine"""
    database_url = URL(**DATABASE_CONN)
    db_engine = create_engine(database_url)
    return db_engine


def create_db_session():
    """ Create database session """
    db_engine = create_db_engine()
    session = sessionmaker(bind=db_engine)
    return session


def create_tables(engine):
    """ Create tables from metadata """
    Base.metadata.create_all(engine)


def drop_tables(engine):
    """ Drop all the tables """
    Base.metadata.drop_all(engine)


def reset_db():
    """ Reset database"""
    db_engine = create_db_engine()
    drop_tables(engine=db_engine)
    create_tables(engine=db_engine)
