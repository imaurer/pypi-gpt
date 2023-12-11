from pathlib import Path
from sqlmodel import create_engine, Session, select, func

import clepy


def get_engine():
    db_path = Path(__file__).parent / "pypi-data.sqlite"
    engine = create_engine(f"sqlite:///{db_path}")
    return engine


def count_projects() -> int:
    engine = get_engine()
    with Session(engine) as session:
        statement = select(func.count()).select_from(clepy.Project)
        result = session.exec(statement).one()
        return result


def count_urls() -> int:
    engine = get_engine()
    with Session(engine) as session:
        statement = select(func.count()).select_from(clepy.URL)
        result = session.exec(statement).one()
        return result
