GROUP_ARTICLES_INSTRUCTION = """You are analyzing a cluster of related news articles to identify meaningful sub-groupings.

All articles provided are about the same overarching story/event. Your task is to determine if there are distinct sub-events, angles, or developments that warrant separate treatment.

Sub-grouping is appropriate when articles cover:
- Distinct events within the same overarching story (e.g., different incidents in an ongoing conflict)
- Different geographic locations where related events occurred
- Different time periods or phases of a developing story
- Significantly different angles or aspects (e.g., political response vs. humanitarian impact)

IMPORTANT: Sub-grouping is OPTIONAL. Many clusters do not need sub-groups because:
- The story is a singular event without distinct sub-parts
- All articles cover the same aspect from different sources
- Forcing sub-groups would be artificial and unhelpful

For each article, you will receive:
- id: unique identifier
- title: the article headline
- summary: brief summary of the article
- published_at: publication timestamp
- source: the publication name

Return a JSON object with:
- needs_subgroups: boolean indicating if sub-grouping is appropriate
- subgroups: an array of sub-group objects (empty if needs_subgroups is false)
  - Each sub-group should have:
    - theme: brief description of what this sub-group covers
    - article_ids: array of article IDs belonging to this sub-group
- reasoning: explanation of why sub-grouping is or isn't appropriate

Articles can only belong to one sub-group. If an article doesn't fit any sub-group well, it can be left out of all sub-groups (it will still be part of the main story)."""
