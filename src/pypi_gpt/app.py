import os

from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from pypi_gpt import ProjectWithURLs, db_queries

# Note:
# I use ngrok (pay-as-you go) for local development with https.
# I use Digital Ocean with nginx and let's encrypt for https.
hostname = os.environ.get("PYPI_GPT_SERVER_HOSTNAME")
assert hostname, "Hostname missing. Must set PYPI_GPT_SERVER_HOSTNAME env var."

app = FastAPI(
    title="PyPI GPT Demo API",
    description="Demonstration of Custom GPT Action using a PyPI database.",
    version="0.1",
    root_path=f"https://{hostname}/pypi_gpt",
    servers=[{"url": f"https://{hostname}/pypi_gpt"}],
)

origins = [
    "http://localhost",
    "https://chat.openai.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{name}/{version}/")
async def get_project(
    name: str = Path(
        ...,
        description="Package name of module.",
        examples=["fastapi"],
    ),
    version: str = Path(
        ...,
        description="Version of module to retrieve.",
        examples=["0.104.1"],
    ),
) -> ProjectWithURLs:
    """Given a"""
    return db_queries.get_project(name, version)
