GENERATE_TITLE_COMPONENT = {
    "task": """## Generate Title

Create a short event label (NOT a full headline) that identifies the story.

Requirements:
- 2-6 words maximum
- Neutral: no opinion, emotion, or sensationalism
- Label-like: e.g., "Cairo Ceasefire Negotiations", "Apple M4 MacBook Pro"

DO NOT:
- Write a full headline or sentence
- Include action verbs (no "resumes", "announces", "reveals")
- Use clickbait or emotional language""",

    "output_field": "title",
    "output_type": "string",
    "output_description": "Short neutral event label (2-6 words)",
    "output_example": '"Gaza Humanitarian Crisis"',
}
