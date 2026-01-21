import json
from openai import OpenAI

from cronkite.instructions import GENERATE_TITLE_INSTRUCTION


def generate_title(articles: list[dict], client: OpenAI, model: str) -> str:
    """
    Generate a clear, descriptive, unbiased headline for a set of articles.

    Args:
        articles: List of article dicts with title, summary, source
        client: OpenAI client instance
        model: Model identifier to use

    Returns:
        Generated headline string
    """
    if not articles:
        return ""

    # Prepare article data for the LLM
    articles_for_llm = [
        {
            "title": article["title"],
            "summary": article["summary"],
            "source": article["source"],
        }
        for article in articles
    ]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": GENERATE_TITLE_INSTRUCTION},
            {"role": "user", "content": json.dumps(articles_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)

    return result.get("title", "")
