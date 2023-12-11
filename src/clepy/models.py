from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    version: str
    author: Optional[str] = None
    author_email: Optional[str] = None
    home_page: Optional[str] = None
    license: Optional[str] = None
    maintainer: Optional[str] = None
    maintainer_email: Optional[str] = None
    package_url: Optional[str] = None
    platform: Optional[str] = None
    project_url: Optional[str] = None
    requires_python: Optional[str] = None
    summary: Optional[str] = None
    yanked: int
    yanked_reason: Optional[str] = None
    classifiers: Optional[str] = None
    requires_dist: Optional[str] = None

    urls: list["URL"] = Relationship(back_populates="project")

    class Config:
        unique_together = [("name", "version")]


class URL(SQLModel, table=True):
    __tablename__ = "urls"

    id: int = Field(default=None, primary_key=True)  # artificial primary key
    project_id: int = Field(foreign_key="project.id")
    url: str
    upload_time: str
    package_type: Optional[str] = None
    python_version: Optional[str] = None
    requires_python: Optional[str] = None
    size: int
    yanked: int
    yanked_reason: Optional[str] = None

    project: Project = Relationship(back_populates="urls")
