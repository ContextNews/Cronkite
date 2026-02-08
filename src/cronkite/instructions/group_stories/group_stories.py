GROUP_STORIES_COMPONENT = {
    "task": """## Group Stories

You are given two groups of news stories: group_a and group_b. Your task is to identify stories across the two groups that cover the same underlying event or development.

**Guidelines:**
- Compare every story in group_a against every story in group_b
- Two stories are a match if they describe the same real-world event, not merely the same broad topic
- For example, two stories about different earthquakes in different countries are NOT a match, but two stories about the same earthquake ARE a match
- A story in one group may match zero, one, or multiple stories in the other group
- Use the story title, summary, and key points to determine matches
- Be precise: only link stories that clearly refer to the same event or development
- Do NOT link stories that are merely topically related""",

    "output_field": "links",
    "output_type": "array of objects",
    "output_description": "Array of link objects, each containing the index of a story in group_a and the index of a matching story in group_b",
    "output_example": '[{"group_a_index": 0, "group_b_index": 2}, {"group_a_index": 1, "group_b_index": 0}]',
}
