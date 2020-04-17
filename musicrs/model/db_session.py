from contextlib import contextmanager
from musicrs.util.db import create_db_session


@contextmanager
def session_scope():
    Session = create_db_session()
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as error:
        session.rollback()
        raise error
    finally:
        session.close()
