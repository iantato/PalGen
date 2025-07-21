from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from palgen.models.base import Base


def get_sessionmaker() -> sessionmaker:
    """Creates a new SQLAlchemy sessionmaker."""
    engine = create_engine('sqlite:///pals.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

@contextmanager
def get_db_session():
    """Context manager for SQLAlchemy database sessions."""
    Session = get_sessionmaker()
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()