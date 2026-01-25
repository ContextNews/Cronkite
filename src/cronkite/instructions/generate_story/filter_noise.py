FILTER_NOISE_COMPONENT = {
    "task": """## Filter Noise

Identify articles that don't belong to the cluster or are noise.

First, identify the core story/event that the majority of articles are about.
Then, evaluate each article to determine if it should be filtered.

An article is NOISE if:
- It does not relate to the core story/event
- It is a generic aggregation article (e.g., "Today's Top Headlines", "Weekly Roundup")
- It only tangentially mentions the story without substantive coverage

Be conservative - only filter articles that clearly don't belong.""",

    "output_field": "noise_article_ids",
    "output_type": "array of strings",
    "output_description": "Array of article IDs to filter out as noise",
    "output_example": '["article-id-1", "article-id-2"]',
}
