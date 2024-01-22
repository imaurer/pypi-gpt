# PyPI GPT

This is an open-source demonstration (MIT License) of building actions for Custom GPTs. It is
built with FastAPI, SQLModel and Pydantic.

This project is NOT associated with [Python Software Foundation](https://www.python.org/psf-landing/)
or the [Python Package Index (PyPI)](https://pypi.org/).

The data used was downloaded from the [pypi-data/pypi-json-data](https://github.com/pypi-data/pypi-json-data)
repository.

If you want to efficiently parse a requirements file, you don't need this project. Instead, use
something like [requirements-parser project](https://pypi.org/project/requirements-parser/).

## Getting Started

### Setup Environment

This project was built using Python 3.11 and the Makefile scripts assume a virtual environment
can be found under the relative path `./env` from the root of the project.

#### Create Environment and Install Dependencies

```bash
    $ python3.11 -m venv env
    $ make sync
```

