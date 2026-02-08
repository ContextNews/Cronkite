import json

from openai import OpenAI

from cronkite.instructions.group_stories import GROUP_STORIES_COMPONENT


def group_stories(
    client: OpenAI,
    model: str,
    group_a: list[dict],
    group_b: list[dict],
) -> list[dict]:
    """
    Link stories across two groups that cover the same underlying event.

    Args:
        client: OpenAI client instance
        model: Model identifier (e.g., "gpt-4o")
        group_a: First list of story dicts with title, summary, key_points, etc.
        group_b: Second list of story dicts with title, summary, key_points, etc.

    Returns:
        List of link dicts, each with "group_a_index" and "group_b_index"
        indicating which stories match across the two groups.
    """
    if not group_a or not group_b:
        return []

    instruction = _build_instruction(GROUP_STORIES_COMPONENT)

    stories_for_llm = {
        "group_a": [
            {
                "index": i,
                "title": story.get("title", ""),
                "summary": story.get("summary", ""),
                "key_points": story.get("key_points", []),
            }
            for i, story in enumerate(group_a)
        ],
        "group_b": [
            {
                "index": i,
                "title": story.get("title", ""),
                "summary": story.get("summary", ""),
                "key_points": story.get("key_points", []),
            }
            for i, story in enumerate(group_b)
        ],
    }

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": json.dumps(stories_for_llm)},
        ],
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)
    return result.get("links", [])


def _build_instruction(component: dict) -> str:
    """Build instruction for story grouping from a component."""
    parts = [
        "You are a news story matching system. You are given two groups of stories and must identify which stories across the groups cover the same underlying event.",
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
