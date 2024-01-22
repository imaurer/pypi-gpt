import instructor

from openai import OpenAI
from pypi_gpt.req_models import RequirementList

client = instructor.patch(OpenAI())


def get_requirement_list(txt: str) -> RequirementList:
    return client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        response_model=RequirementList,
        messages=[
            {
                "role": "user",
                "content": f"Parse the following requirements.txt: {txt}",
            },
        ],
    )  # type: ignore


if __name__ == "__main__":
    requirement_list = get_requirement_list(
        """
pytest==7.0.1
mypy==1.4.1
black>=22.10,<24.0
mkdocs-material==9.2.7
pillow==9.3.0
cairosvg==2.5.2
mdx-include==1.4.1
coverage[toml]>=6.2,<8.0
fastapi==0.103.2
ruff==0.1.2
httpx==0.24.1
dirty-equals==0.6.0
typer-cli==0.0.13
mkdocs-markdownextradata-plugin>=0.1.7,<0.3.0
    """
    )

    print(requirement_list.model_dump_json(indent=2))
