import json

from openai import OpenAI

from cronkite.instructions.classify_stories import CLASSIFY_STORIES_COMPONENT


def classify_stories(
    client: OpenAI,
    model: str,
    stories: list[dict],
) -> list[dict]:
    """
    Classify stories by topic.

    Args:
        client: OpenAI client instance
        model: Model identifier (e.g., "gpt-4o")
        stories: List of story dicts with title, summary, key_points, etc.

    Returns:
        List of story dicts with 'topics' field added to each
    """
    if not stories:
        return []

    instruction = _build_instruction(CLASSIFY_STORIES_COMPONENT)
    stories_for_llm = [
        {
            "index": i,
            "title": story.get("title", ""),
            "summary": story.get("summary", ""),
            "key_points": story.get("key_points", []),
        }
        for i, story in enumerate(stories)
    ]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": json.dumps(stories_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)
    classifications = {
        c["story_index"]: c["topics"]
        for c in result.get("classifications", [])
    }

    return [
        {**story, "topics": classifications.get(i, [])}
        for i, story in enumerate(stories)
    ]


def _build_instruction(component: dict) -> str:
    """Build instruction for classification from a component."""
    parts = [
        "You are a news classification system. Analyze the provided stories and classify them by topic.",
        "",
        component["task"],
        "",
        "## Expected Output",
        "",
        "Return a JSON object with the following structure:",
        "{",
        f'    "{component["output_field"]}": ...  // {component["output_description"]}',
        "}",
        "",
        "Field details:",
        f'- {component["output_field"]} ({component["output_type"]}): e.g., {component["output_example"]}',
    ]
    return "\n".join(parts)
