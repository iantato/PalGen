import os
from contextlib import contextmanager
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from palgen.models.base import Base
from palgen.models.pal_model import Pal, PalTable

def get_sessionmaker(output_path: str) -> sessionmaker:
    """Creates a new SQLAlchemy sessionmaker."""
    engine = create_engine(f'sqlite:///{output_path}/pals.db')
    Base.metadata.create_all(engine)
    logger.debug(f"Database created at {output_path}/pals.db")
    return sessionmaker(bind=engine)

@contextmanager
def get_db_session(output_path: str):
    """Context manager for SQLAlchemy database sessions."""
    Session = get_sessionmaker(output_path)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"An error occurred while processing the database session: {e}")
        raise e
    finally:
        session.close()

def save_pals_to_db(pals: list[Pal], output_path: str) -> None:
    """Saves a list of Pal objects to the database."""
    # Ensure the database file is removed before creating a new one.
    # Needed for updating the database when needed.
    if os.path.exists(f'{output_path}/pals.db'):
        os.remove(f'{output_path}/pals.db')

    with get_db_session(output_path) as session:
        for pal in pals:
            pal_table = PalTable(**pal.model_dump())
            session.add(pal_table)
            logger.debug(f"Saved Pal to DB: {pal.text_name} (Internal Index: {pal.internal_index})")