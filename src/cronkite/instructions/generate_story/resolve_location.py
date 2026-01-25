RESOLVE_LOCATION_COMPONENT = {
    "task": """## Resolve Story Location

Determine the primary geographic location where the story takes place.

Requirements:
- Identify the most relevant location for the story
- If the story spans multiple locations, choose the primary/most significant one
- Extract as much location detail as can be determined from the articles

Location fields:
- country: ISO3 country code (e.g., "USA", "GBR", "CHN")
- region: State, province, or region (e.g., "California", "England")
- city: City or town (e.g., "Los Angeles", "London")

If a location level cannot be determined, use null for that field.""",

    "output_field": "location",
    "output_type": "object",
    "output_description": "Object with country (ISO3), region, and city fields (null if unknown)",
    "output_example": '{"country": "USA", "region": "California", "city": "Los Angeles"}',
}
