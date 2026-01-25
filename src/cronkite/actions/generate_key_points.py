import json
from openai import OpenAI

from cronkite.instructions import GENERATE_KEY_POINTS_INSTRUCTION


def generate_key_points(articles: list[dict], client: OpenAI, model: str) -> list[str]:
    """
    Generate 3-6 key points summarizing the main facts from articles.

    Args:
        articles: List of article dicts with title, summary, text, source, published_at
        client: OpenAI client instance
        model: Model identifier to use

    Returns:
        List of key point strings (3-6 items)
    """
    if not articles:
        return []

    # Prepare article data for the LLM
    articles_for_llm = [
        {
            "title": article["title"],
            "summary": article["summary"],
            "text": article["text"],
            "source": article["source"],
            "published_at": article["published_at"],
        }
        for article in articles
    ]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": GENERATE_KEY_POINTS_INSTRUCTION},
            {"role": "user", "content": json.dumps(articles_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)

    return result.get("key_points", [])
