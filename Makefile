ACTIVATE = . ./activate.sh

test:
	$(ACTIVATE) && pytest -s tests/

cov:
	$(ACTIVATE) && coverage run -m pytest -s tests && coverage combine && coverage report --show-missing && coverage html

sync:
	$(ACTIVATE) && pip install --upgrade pip && pip install ".[test]"

api:
	$(ACTIVATE) && uvicorn clepy:app --reload --port 8010
