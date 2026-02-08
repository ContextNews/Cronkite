from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

from cronkite.config import CronkiteConfig
from cronkite.actions import generate_story as _generate_story
from cronkite.actions import classify_stories as _classify_stories
from cronkite.actions import group_stories as _group_stories


class Cronkite:
    """
    LLM-powered agent that generates cohesive news stories from article clusters.
    """

    def __init__(self, model: str = "gpt-4o", config: CronkiteConfig | None = None):
        """
        Initialize Cronkite with a configurable OpenAI model and pipeline config.

        Args:
            model: OpenAI model identifier (e.g., "gpt-4o", "gpt-4o-mini")
            config: Pipeline configuration. Defaults to all actions enabled.
        """
        self.model = model
        self.config = config or CronkiteConfig()
        self.client = OpenAI()

    def generate_story(self, articles: list[dict]) -> dict:
        """
        Process articles through unified pipeline and return a story.

        Args:
            articles: List of article dicts with id, title, summary, text,
                      published_at, source

        Returns:
            Story dict with title, summary, key_points, quotes, sub_stories,
            article_ids, noise_article_ids
        """
        return _generate_story(self.client, self.model, articles, self.config)

    def classify_stories(self, stories: list[dict]) -> list[dict]:
        """
        Classify stories by topic.

        Args:
            stories: List of story dicts with title, summary, key_points, etc.

        Returns:
            List of story dicts with 'topics' field added to each
        """
        return _classify_stories(self.client, self.model, stories)

    def group_stories(self, group_a: list[dict], group_b: list[dict]) -> list[dict]:
        """
        Link stories across two groups that cover the same underlying event.

        Args:
            group_a: First list of story dicts with title, summary, key_points, etc.
            group_b: Second list of story dicts with title, summary, key_points, etc.

        Returns:
            List of link dicts, each with "group_a_index" and "group_b_index"
            indicating which stories match across the two groups.
        """
        return _group_stories(self.client, self.model, group_a, group_b)
