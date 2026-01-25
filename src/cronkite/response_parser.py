from cronkite.config import CronkiteConfig


# Default values for each field when action is disabled
FIELD_DEFAULTS = {
    "noise_article_ids": [],
    "subgroups": [],
    "title": "",
    "summary": "",
    "key_points": [],
    "quotes": [],
    "location": None,
}


def parse_response(response: dict, config: CronkiteConfig, articles: list[dict]) -> dict:
    """
    Parse LLM response and structure it according to output schema.

    Args:
        response: Raw JSON response from LLM
        config: CronkiteConfig indicating which actions were enabled
        articles: Original articles list (for computing article_ids)

    Returns:
        Structured story dict with all fields populated
    """
    # Get noise_article_ids to filter articles
    noise_ids = set(response.get("noise_article_ids", []) if config.filter_noise else [])

    # Compute filtered article IDs
    filtered_article_ids = [a["id"] for a in articles if a["id"] not in noise_ids]

    # Build story dict
    story = {
        "title": _get_field(response, "title", config.generate_title),
        "summary": _get_field(response, "summary", config.generate_summary),
        "key_points": _get_field(response, "key_points", config.generate_key_points),
        "quotes": _get_field(response, "quotes", config.extract_quotes),
        "location": _get_field(response, "location", config.resolve_location),
        "sub_stories": [],  # Populated separately after substory generation
        "article_ids": filtered_article_ids,
        "noise_article_ids": list(noise_ids),
    }

    return story


def _get_field(response: dict, field: str, enabled: bool):
    """Get field value from response if enabled, otherwise return default."""
    if enabled:
        return response.get(field, FIELD_DEFAULTS.get(field))
    return FIELD_DEFAULTS.get(field)


def get_subgroups(response: dict, config: CronkiteConfig) -> list[dict]:
    """Extract subgroups from response if grouping was enabled."""
    if config.group_articles:
        return response.get("subgroups", [])
    return []


def get_filtered_articles(articles: list[dict], response: dict, config: CronkiteConfig) -> list[dict]:
    """
    Get articles after filtering noise.

    Args:
        articles: Original articles list
        response: LLM response containing noise_article_ids
        config: Config indicating if filtering was enabled

    Returns:
        Filtered list of articles
    """
    if not config.filter_noise:
        return articles

    noise_ids = set(response.get("noise_article_ids", []))
    return [a for a in articles if a["id"] not in noise_ids]
