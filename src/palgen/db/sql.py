import os
from contextlib import contextmanager
from loguru import logger
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from palgen.models.base import Base
from palgen.models.pal_model import Pal, PalTable
from palgen.models.combiunique_model import CombiUniqueModel, CombiUniqueTable

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

def clear_content(session, table):
    if os.path.exists(session.bind.url.database):
        session.execute(delete(table))
        session.commit()
        logger.debug(f"Cleared content from table {table.__tablename__}")

def save_pals_to_db(pals: list[Pal], output_path: str) -> None:
    """Saves a list of Pal objects to the database."""
    with get_db_session(output_path) as session:

        clear_content(session, PalTable)

        for pal in pals:
            pal_table = PalTable(**pal.model_dump())
            session.add(pal_table)
            logger.debug(f"Saved Pal to DB: {pal.text_name} (Internal Index: {pal.internal_index})")

def save_unique_combinations_to_db(combinations: list[CombiUniqueModel], output_path: str) -> None:
    with get_db_session(output_path) as session:

        clear_content(session, CombiUniqueTable)

        for combi in combinations:
            combi_table = CombiUniqueTable(**combi.model_dump())
            session.add(combi_table)
            logger.debug(f"Saved Combi Unique to DB: {combi.child_id} with parents {combi.parents}")