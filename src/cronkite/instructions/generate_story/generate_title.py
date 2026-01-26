GENERATE_TITLE_COMPONENT = {
    "task": """Generate a short, neutral event title.

Rules:
- 3–7 words
- Factual, encyclopedic tone
- Event-focused (what happened)
- Simple verbs allowed (e.g. Bombs, Approves, Exits, Hits)

Avoid:
- Emotion, opinion, or hype
- Clickbait phrasing
- Full sentences or punctuation

Examples:
- US Bombs Iranian Energy Infrastructure
- UK To Establish National Police Service
- Gold Prices Hit All-Time High
- Amazon To Exit Japanese Market
- New York Protests Grow""",

    "output_field": "title",
    "output_type": "string",
    "output_description": "Short, neutral event title (3-7 words)",
    "output_example": '"US Bombs Iranian Energy Infrastructure"',
}
