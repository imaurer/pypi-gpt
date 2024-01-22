from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from pypi_gpt import ProjectWithURLs, db_queries

app = FastAPI(title="ClePy 12/11")

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
    name: str = Path(...),
    version: str = Path(...),
) -> ProjectWithURLs:
    return db_queries.get_project(name, version)
