GENERATE_SUMMARY_COMPONENT = {
    "task": """## Generate Summary

Synthesize the key information into a single, dense paragraph.

Requirements:
- One paragraph, 150-200 words maximum
- Factual and neutral - no editorializing
- Covers the essential who, what, when, where, why
- Synthesizes information from multiple sources
- Acknowledges disputes or uncertainty where sources disagree

Guidelines:
- Be concise - every word should earn its place
- Prioritize facts that appear in multiple sources
- No sensationalism or emotional language""",

    "output_field": "summary",
    "output_type": "string",
    "output_description": "Condensed single-paragraph summary (150-200 words)",
    "output_example": '"Summary text here..."',
}
