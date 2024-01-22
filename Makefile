SHELL := /bin/bash
ACTIVATE = . ./activate.sh

install:
	$(ACTIVATE) && pip install --upgrade pip && pip install ".[test]"

download_db:
	wget -O ./src/pypi_gpt/pypi-data.sqlite.gz https://github.com/pypi-data/pypi-json-data/releases/download/latest/pypi-data.sqlite.gz
	gunzip ./src/pypi_gpt/pypi-data.sqlite.gz
	sqlite3 ./src/pypi_gpt/pypi-data.sqlite < prep_db.sql

test:
	$(ACTIVATE) && pytest -s tests/

cov:
	$(ACTIVATE) && coverage run -m pytest -s tests && coverage combine && coverage report --show-missing && coverage html

api:
	$(ACTIVATE) && uvicorn pypi_gpt:app --host 0.0.0.0 --port 8000
