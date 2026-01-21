import json
from openai import OpenAI

from cronkite.instructions import GENERATE_SUMMARY_INSTRUCTION


def generate_summary(articles: list[dict], client: OpenAI, model: str) -> str:
    """
    Generate a comprehensive, neutral summary synthesizing information from articles.

    Args:
        articles: List of article dicts with title, summary, text, source, published_at
        client: OpenAI client instance
        model: Model identifier to use

    Returns:
        Generated summary string (2-4 paragraphs)
    """
    if not articles:
        return ""

    # Prepare article data for the LLM (include full text for summary generation)
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
            {"role": "system", "content": GENERATE_SUMMARY_INSTRUCTION},
            {"role": "user", "content": json.dumps(articles_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)

    return result.get("summary", "")
