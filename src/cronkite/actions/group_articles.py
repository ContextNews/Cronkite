import json
from openai import OpenAI

from cronkite.instructions import GROUP_ARTICLES_INSTRUCTION


def group_articles(articles: list[dict], client: OpenAI, model: str) -> list[dict]:
    """
    Identify sub-groupings within a cluster of related articles.

    Args:
        articles: List of article dicts with id, title, summary, published_at, source
        client: OpenAI client instance
        model: Model identifier to use

    Returns:
        List of sub-group dicts, each with 'theme' and 'article_ids'.
        Empty list if no sub-grouping is needed.
    """
    if not articles or len(articles) < 2:
        return []

    # Prepare article data for the LLM
    articles_for_llm = [
        {
            "id": article["id"],
            "title": article["title"],
            "summary": article["summary"],
            "published_at": article["published_at"],
            "source": article["source"],
        }
        for article in articles
    ]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": GROUP_ARTICLES_INSTRUCTION},
            {"role": "user", "content": json.dumps(articles_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)

    if not result.get("needs_subgroups", False):
        return []

    return result.get("subgroups", [])
