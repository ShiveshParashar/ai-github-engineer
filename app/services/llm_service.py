import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Project root: ai-github-engineer/
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env from project root
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        f"OPENAI_API_KEY not found. Expected .env at: {BASE_DIR / '.env'}"
    )

client = OpenAI(api_key=api_key)


def generate_repository_summary(repository_data: dict) -> str:
    prompt = f"""
    Analyze the following GitHub repository information.

    Repository data:
    {repository_data}

    Include:
    - Project purpose
    - Main technologies
    - Project structure
    - Important observations
    - Potential improvements
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text