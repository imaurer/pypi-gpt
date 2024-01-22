import json
from typing import Optional, List

from pydantic import field_serializer
from sqlmodel import Field, SQLModel, Relationship


class ProjectBase(SQLModel):
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


class Project(ProjectBase, table=True):
    __tablename__ = "projects"
    urls: List["URL"] = Relationship(back_populates="project")

    class Config:
        unique_together = [("name", "version")]


class URL(SQLModel, table=True):
    __tablename__ = "urls"

    project_id: int = Field(
        foreign_key="projects.id",
        primary_key=True,
    )
    url: str = Field(primary_key=True)
    upload_time: str
    package_type: Optional[str] = None
    python_version: Optional[str] = None
    requires_python: Optional[str] = None
    size: int
    yanked: int
    yanked_reason: Optional[str] = None

    project: Project = Relationship(back_populates="urls")


class ProjectWithURLs(ProjectBase):
    urls: List[URL] = Field(default_factory=list)

    @field_serializer("classifiers", "requires_dist")
    def serialize_json(self, value):
        if isinstance(value, str):
            return json.loads(value)
        return value
