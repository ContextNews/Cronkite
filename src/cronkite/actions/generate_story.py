import json

from openai import OpenAI

from cronkite.config import CronkiteConfig
from cronkite.instruction_builder import build_instruction
from cronkite.response_parser import (
    parse_response,
    get_subgroups,
    get_filtered_articles,
)


def generate_story(
    client: OpenAI,
    model: str,
    articles: list[dict],
    config: CronkiteConfig,
) -> dict:
    """
    Process articles through unified pipeline and return a story.

    Args:
        client: OpenAI client instance
        model: Model identifier (e.g., "gpt-4o")
        articles: List of article dicts with id, title, summary, text,
                  published_at, source
        config: Pipeline configuration

    Returns:
        Story dict with title, summary, key_points, quotes, sub_stories,
        article_ids, noise_article_ids
    """
    if not articles:
        return _empty_story()

    instruction = build_instruction(config)
    response = _call_llm(client, model, instruction, articles)

    filtered_articles = get_filtered_articles(articles, response, config)
    if not filtered_articles:
        return {
            **_empty_story(),
            "noise_article_ids": [a["id"] for a in articles],
        }

    story = parse_response(response, config, articles)

    if config.generate_substories:
        subgroups = get_subgroups(response, config)
        if subgroups:
            story["sub_stories"] = [
                _generate_substory(client, model, subgroup, filtered_articles)
                for subgroup in subgroups
            ]

    return story


def _call_llm(
    client: OpenAI,
    model: str,
    instruction: str,
    articles: list[dict],
) -> dict:
    """Make a single LLM call with the given instruction and articles."""
    articles_for_llm = [
        {
            "id": article["id"],
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
            {"role": "system", "content": instruction},
            {"role": "user", "content": json.dumps(articles_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


def _generate_substory(
    client: OpenAI,
    model: str,
    subgroup: dict,
    all_articles: list[dict],
) -> dict:
    """Generate a substory for a sub-group of articles."""
    article_ids = set(subgroup.get("article_ids", []))
    subgroup_articles = [a for a in all_articles if a["id"] in article_ids]

    if not subgroup_articles:
        return {
            "title": subgroup.get("theme", ""),
            "summary": "",
            "article_ids": [],
        }

    substory_config = CronkiteConfig(
        filter_noise=False,
        group_articles=False,
        generate_title=True,
        generate_summary=True,
        generate_key_points=False,
        extract_quotes=False,
        generate_substories=False,
    )

    instruction = build_instruction(substory_config)
    response = _call_llm(client, model, instruction, subgroup_articles)

    return {
        "title": response.get("title", subgroup.get("theme", "")),
        "summary": response.get("summary", ""),
        "article_ids": list(article_ids),
    }


def _empty_story() -> dict:
    """Return an empty story structure."""
    return {
        "title": "",
        "summary": "",
        "key_points": [],
        "quotes": [],
        "location": None,
        "sub_stories": [],
        "article_ids": [],
        "noise_article_ids": [],
    }
