import json
from openai import OpenAI

from cronkite.instructions import EXTRACT_QUOTES_INSTRUCTION


def extract_quotes(articles: list[dict], client: OpenAI, model: str) -> list[dict]:
    """
    Extract notable quotes from articles.

    Args:
        articles: List of article dicts with id, title, text, source
        client: OpenAI client instance
        model: Model identifier to use

    Returns:
        List of quote dicts with text, speaker_name, speaker_title,
        speaker_org, speaker_nation, article_id
    """
    if not articles:
        return []

    # Prepare article data for the LLM (include full text for quote extraction)
    articles_for_llm = [
        {
            "id": article["id"],
            "title": article["title"],
            "text": article["text"],
            "source": article["source"],
        }
        for article in articles
    ]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": EXTRACT_QUOTES_INSTRUCTION},
            {"role": "user", "content": json.dumps(articles_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)

    return result.get("quotes", [])
