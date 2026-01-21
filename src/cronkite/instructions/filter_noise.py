FILTER_NOISE_INSTRUCTION = """You are analyzing a cluster of news articles to identify and filter out noise.

Your task is to:
1. First, identify the core story/event that the majority of articles are about
2. Then, evaluate each article to determine if it belongs to this cluster or is noise

An article should be classified as NOISE if:
- It does not relate to the core story/event of the cluster
- It is a generic aggregation article (e.g., "Today's Top Headlines", "Weekly News Roundup", "Morning Briefing", "What You Need to Know Today")
- It only tangentially mentions the story without substantive coverage
- It is a duplicate or near-duplicate of another article from the same source

For each article, you will receive:
- id: unique identifier
- title: the article headline
- summary: brief summary of the article
- source: the publication name

Analyze the articles and return a JSON object with:
- core_story: A brief description of what the main story/event is about
- noise_article_ids: An array of article IDs that should be filtered out as noise
- reasoning: An object mapping each noise article ID to a brief explanation of why it was classified as noise

Be conservative - only filter articles that clearly don't belong. When in doubt, keep the article."""
