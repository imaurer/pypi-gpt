from fastapi import FastAPI

app = FastAPI(
    title="ClePy 12/11",
    summary="Demonstration of FastAPI, Pydantic, and OpenAI GPTS.",
    description="""
Supports `markdown` including:
- Bullets
- And other things.
    """.strip(),
    version="0.1.0.beta12345",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}