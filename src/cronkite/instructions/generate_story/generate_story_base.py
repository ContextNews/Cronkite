BASE_PREAMBLE = """You are analyzing a cluster of news articles about the same story/event.

For each article, you will receive:
- id: unique identifier
- title: the article headline
- summary: brief summary of the article
- text: the full article text
- source: the publication name
- published_at: publication timestamp

Your task is to process these articles and return a JSON object with the requested fields.
"""
