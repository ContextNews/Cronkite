GENERATE_KEY_POINTS_INSTRUCTION = """You are extracting key points from a news story based on multiple source articles.

Your task is to identify 3-6 key points that capture the most important facts and developments.

Requirements:
- Generate between 3 and 6 key points
- Each point should be a single, concise sentence
- Factual and neutral - no editorializing
- Cover the most significant facts, developments, or takeaways
- Prioritize information that appears across multiple sources

For each article, you will receive:
- title: the article headline
- summary: brief summary of the article
- text: the full article text
- source: the publication name
- published_at: publication timestamp

Guidelines:
- Each key point should stand alone and be understandable without context
- Avoid redundancy between points
- Order points by importance (most important first)
- Use clear, straightforward language
- No sensationalism or emotional language

Return a JSON object with:
- key_points: array of strings, each string being one key point (3-6 items)"""
