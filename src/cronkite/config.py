from dataclasses import dataclass


@dataclass
class CronkiteConfig:
    """Configuration for which pipeline actions to run."""

    filter_noise: bool = True
    group_articles: bool = True
    generate_title: bool = True
    generate_summary: bool = True
    generate_key_points: bool = True
    extract_quotes: bool = True
    generate_substories: bool = True
