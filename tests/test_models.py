from clepy import db


def test_counts():
    n_projects = db.count_projects()
    assert n_projects == 5288639

    n_urls = db.count_urls()
    assert n_urls == 10123064
