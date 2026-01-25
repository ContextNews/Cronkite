from cronkite.config import CronkiteConfig
from cronkite.instructions.generate_story import (
    BASE_PREAMBLE,
    FILTER_NOISE_COMPONENT,
    GROUP_ARTICLES_COMPONENT,
    GENERATE_TITLE_COMPONENT,
    GENERATE_SUMMARY_COMPONENT,
    GENERATE_KEY_POINTS_COMPONENT,
    EXTRACT_QUOTES_COMPONENT,
    RESOLVE_LOCATION_COMPONENT,
)


def build_instruction(config: CronkiteConfig) -> str:
    """
    Build a combined instruction based on enabled config options.

    Returns a system prompt that includes only the relevant task
    descriptions for enabled actions.
    """
    parts = [BASE_PREAMBLE]

    # Collect enabled components
    components = _get_enabled_components(config)

    # Add task descriptions
    for component in components:
        parts.append(component["task"])

    # Add output schema
    parts.append(_build_output_schema(components))

    return "\n".join(parts)


def _get_enabled_components(config: CronkiteConfig) -> list[dict]:
    """Get list of enabled components based on config."""
    components = []

    if config.filter_noise:
        components.append(FILTER_NOISE_COMPONENT)
    if config.group_articles:
        components.append(GROUP_ARTICLES_COMPONENT)
    if config.generate_title:
        components.append(GENERATE_TITLE_COMPONENT)
    if config.generate_summary:
        components.append(GENERATE_SUMMARY_COMPONENT)
    if config.generate_key_points:
        components.append(GENERATE_KEY_POINTS_COMPONENT)
    if config.extract_quotes:
        components.append(EXTRACT_QUOTES_COMPONENT)
    if config.resolve_location:
        components.append(RESOLVE_LOCATION_COMPONENT)

    return components


def _build_output_schema(components: list[dict]) -> str:
    """Build the expected output schema section."""
    if not components:
        return "Return an empty JSON object: {}"

    lines = ["## Expected Output", "", "Return a JSON object with the following structure:", "{"]

    schema_lines = []
    for component in components:
        field = component["output_field"]
        description = component["output_description"]
        example = component["output_example"]
        schema_lines.append(f'    "{field}": ...  // {description}')

    lines.append(",\n".join(schema_lines))
    lines.append("}")

    # Add field details
    lines.append("")
    lines.append("Field details:")
    for component in components:
        field = component["output_field"]
        output_type = component["output_type"]
        example = component["output_example"]
        lines.append(f"- {field} ({output_type}): e.g., {example}")

    return "\n".join(lines)


def get_enabled_fields(config: CronkiteConfig) -> list[str]:
    """Get list of output field names for enabled actions."""
    components = _get_enabled_components(config)
    return [c["output_field"] for c in components]
