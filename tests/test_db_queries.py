from pypi_gpt import db_queries, Project, URL


def test_counts():
    # counts last updated for 2024-01-22
    n_projects = db_queries.count_table(Project)
    assert n_projects >= 5429927
    n_urls = db_queries.count_table(URL)
    assert n_urls >= 10459795


def test_get_project():
    project = db_queries.get_project(name="fastapi", version="0.104.1")

    assert project.name == "fastapi"
    assert project.author_email == "Sebastián Ramírez <tiangolo@gmail.com>"
    assert project.summary == (
        "FastAPI framework, high performance, easy to "
        "learn, fast to code, ready for production"
    )
    assert len(project.urls) == 2
