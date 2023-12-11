from fastapi import FastAPI, Path
from clepy import Project, db

app = FastAPI(title="ClePy 12/11")


@app.get("/{name}/{version}/")
async def get_project(
    name: str = Path(...),
    version: str = Path(...),
) -> Project:
    return db.get_project(name, version)
