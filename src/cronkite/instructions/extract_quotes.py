EXTRACT_QUOTES_INSTRUCTION = """You are extracting notable quotes from news articles.

Your task is to identify and extract direct quotes that add value to the story. For each quote, extract as much speaker information as can be determined from context.

Quote selection criteria:
- Must be direct quotes (in quotation marks in the original article)
- Prioritize quotes from key figures (officials, witnesses, experts, stakeholders)
- Select quotes that provide insight, context, or notable perspectives
- Avoid redundant quotes that say essentially the same thing
- Prioritize quotes that add information beyond what's in the summary
- Limit to 5-10 of the most valuable quotes total

For each article, you will receive:
- id: unique identifier (use this as article_id in your response)
- title: the article headline
- text: the full article text
- source: the publication name

For each quote, extract:
- text: the exact quote (as it appears in the article)
- speaker_name: name of the speaker (e.g., "Kash Patel") - null if unknown
- speaker_title: title or role (e.g., "FBI Director") - null if unknown
- speaker_org: organization (e.g., "FBI") - null if unknown
- speaker_nation: ISO3 country code (e.g., "USA", "GBR", "CHN") - null if unknown
- article_id: the ID of the article this quote came from

Note: Not all speaker fields will be available. Extract what you can determine from the article context. It's acceptable to have quotes with only a name, or only an organization, etc.

Return a JSON object with:
- quotes: array of quote objects with the fields described above"""
