import json
from openai import OpenAI

from cronkite.instructions import FILTER_NOISE_INSTRUCTION


def filter_noise(articles: list[dict], client: OpenAI, model: str) -> tuple[list[dict], list[str]]:
    """
    Filter noise articles from a cluster.

    Args:
        articles: List of article dicts with id, title, summary, source
        client: OpenAI client instance
        model: Model identifier to use

    Returns:
        Tuple of (filtered_articles, noise_article_ids)
    """
    if not articles:
        return [], []

    # Prepare article data for the LLM (exclude full text to save tokens)
    articles_for_llm = [
        {
            "id": article["id"],
            "title": article["title"],
            "summary": article["summary"],
            "source": article["source"],
        }
        for article in articles
    ]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": FILTER_NOISE_INSTRUCTION},
            {"role": "user", "content": json.dumps(articles_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)
    noise_ids = set(result.get("noise_article_ids", []))

    filtered_articles = [a for a in articles if a["id"] not in noise_ids]

    return filtered_articles, list(noise_ids)
