GENERATE_KEY_POINTS_COMPONENT = {
    "task": """## Generate Key Points

Identify 3-6 key points capturing the most important facts and developments.

Requirements:
- Generate between 3 and 6 key points
- Each point should be a single, concise sentence
- Factual and neutral - no editorializing
- Cover the most significant facts, developments, or takeaways
- Prioritize information that appears across multiple sources

Guidelines:
- Each key point should stand alone and be understandable without context
- Avoid redundancy between points
- Order points by importance (most important first)""",

    "output_field": "key_points",
    "output_type": "array of strings",
    "output_description": "Array of 3-6 key point sentences",
    "output_example": '["Key point 1.", "Key point 2.", "Key point 3."]',
}
