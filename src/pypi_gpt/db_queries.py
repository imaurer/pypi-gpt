from pathlib import Path
from typing import Type

from sqlmodel import create_engine, Session, select, func, SQLModel

from pypi_gpt import Project, ProjectWithURLs

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        db_path = Path(__file__).parent / "pypi-data.sqlite"
        _engine = create_engine(f"sqlite:///{db_path}")
    return _engine


def count_table(table: Type[SQLModel]) -> int:
    engine = get_engine()
    with Session(engine) as session:
        statement = select(func.count()).select_from(table)
        result = session.exec(statement).one()
        return result


def get_project(name: str, version: str) -> ProjectWithURLs:
    with Session(get_engine()) as session:
        statement = select(Project).where(
            Project.name == name,
            Project.version == version,
        )
        project = session.exec(statement).first()

        # todo: figure out how to handle relationships..
        assert project.urls
        return project
