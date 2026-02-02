CLASSIFY_STORIES_COMPONENT = {
    "task": """## Classify Stories

For each story provided, assign one or more topic classifications from the following categories:

**Available Topics:**
- **Politics** – elections, government, policy, diplomacy
- **Conflict & Security** – wars, terrorism, military, defense
- **Crime** – crime, policing, public safety, corruption, criminal trials
- **Business** – companies, markets, earnings, trade
- **Economy** – inflation, jobs, GDP, interest rates, public finance
- **Technology** – AI, software, hardware, cybersecurity, space, research
- **Health** – public health, outbreaks, healthcare systems
- **Environment** – climate, energy, disasters, conservation
- **Society** – culture, education, demographics, social issues
- **Sports** – all competitive sport
- **Entertainment** – film, TV, music, celebrities

**Guidelines:**
- Assign ALL relevant topics that apply to each story
- Most stories will have 1-3 topics; complex stories may have more
- Use the story title, summary, and key points to determine classification
- Be precise: only assign topics that are central to the story, not tangentially mentioned
- Use exact topic names as listed above (case-sensitive)""",

    "output_field": "classifications",
    "output_type": "array of objects",
    "output_description": "Array of classification objects, one per story, each containing the story index and assigned topics",
    "output_example": '[{"story_index": 0, "topics": ["Politics", "Conflict & Security"]}, {"story_index": 1, "topics": ["Technology", "Business"]}]',
}
