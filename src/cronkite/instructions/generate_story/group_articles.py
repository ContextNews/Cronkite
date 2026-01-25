GROUP_ARTICLES_COMPONENT = {
    "task": """## Group Articles

Identify if there are distinct sub-events within the main story that warrant separate treatment.

IMPORTANT: Not every article needs to be in a sub-group. Articles that cover the overall story broadly should NOT be placed in any sub-group.

Sub-groups are for articles specifically about:
- A specific incident within a larger ongoing story
- Events at a particular location distinct from the main narrative
- A clearly separate development that could stand alone

DO NOT create sub-groups just to categorize by topic. If no clear sub-events exist, return an empty array.""",

    "output_field": "subgroups",
    "output_type": "array of objects",
    "output_description": "Array of sub-group objects, each with 'theme' (string) and 'article_ids' (array of strings). Empty array if no sub-grouping needed.",
    "output_example": '[{"theme": "Hospital strike in northern region", "article_ids": ["id1", "id2"]}]',
}
