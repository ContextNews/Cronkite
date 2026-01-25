EXTRACT_QUOTES_COMPONENT = {
    "task": """## Extract Quotes

Extract notable direct quotes that add value to the story.

Quote selection criteria:
- Must be direct quotes (in quotation marks in the original article)
- Prioritize quotes from key figures (officials, witnesses, experts)
- Select quotes that provide insight, context, or notable perspectives
- Avoid redundant quotes saying essentially the same thing
- Limit to 5-10 of the most valuable quotes

For each quote, extract:
- text: the exact quote
- speaker_name: name of the speaker (null if unknown)
- speaker_title: title or role (null if unknown)
- speaker_org: organization (null if unknown)
- speaker_nation: ISO3 country code (null if unknown)
- article_id: the ID of the source article

Note: Not all speaker fields will be available - extract what you can determine.""",

    "output_field": "quotes",
    "output_type": "array of objects",
    "output_description": "Array of quote objects with text, speaker_name, speaker_title, speaker_org, speaker_nation, article_id",
    "output_example": '[{"text": "Quote here", "speaker_name": "John Smith", "speaker_title": "Director", "speaker_org": "FBI", "speaker_nation": "USA", "article_id": "article-1"}]',
}
