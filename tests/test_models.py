from clepy import db, Project, URL


def test_counts():
    n_projects = db.count_table(Project)
    assert n_projects == 5288639

    n_urls = db.count_table(URL)
    assert n_urls == 10123064


def test_get_project():
    project = db.get_project(name="fastapi", version="0.104.1")

    assert project.name == "fastapi"
    assert project.author_email == "Sebastián Ramírez <tiangolo@gmail.com>"
    assert project.summary == (
        "FastAPI framework, high performance, easy to "
        "learn, fast to code, ready for production"
    )
    assert len(project.urls) == 2
