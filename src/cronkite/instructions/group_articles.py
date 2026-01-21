GROUP_ARTICLES_INSTRUCTION = """You are analyzing a cluster of related news articles to identify if there are distinct sub-events within the main story.

All articles are about the same overarching story/event. Your task is to identify if some articles are specifically about distinct sub-events that warrant separate treatment.

IMPORTANT: Not every article needs to be in a sub-group. Articles that cover the overall story, provide general updates, or don't fit a specific sub-event should NOT be placed in any sub-group. They remain part of the main story only.

Sub-groups are for articles that are specifically and primarily about a distinct sub-event, such as:
- A specific incident within a larger ongoing story
- Events at a particular location that are distinct from the main narrative
- A clearly separate development that could stand alone

DO NOT create sub-groups just to categorize articles by topic or angle. If an article covers the main story broadly (e.g., overall death toll, general international response, summary of events), leave it ungrouped.

For each article, you will receive:
- id: unique identifier
- title: the article headline
- summary: brief summary of the article
- published_at: publication timestamp
- source: the publication name

Return a JSON object with:
- needs_subgroups: boolean indicating if any sub-grouping is appropriate
- subgroups: an array of sub-group objects (empty if needs_subgroups is false)
  - Each sub-group should have:
    - theme: brief description of the distinct sub-event
    - article_ids: array of article IDs specifically about this sub-event
- reasoning: explanation of your grouping decisions

Remember: Many (often most) articles should remain ungrouped, belonging only to the main story."""
