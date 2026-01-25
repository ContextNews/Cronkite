import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

from cronkite.config import CronkiteConfig
from cronkite.instruction_builder import build_instruction
from cronkite.response_parser import (
    parse_response,
    get_subgroups,
    get_filtered_articles,
)


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
        if not articles:
            return self._empty_story()

        # Build instruction based on config
        instruction = build_instruction(self.config)

        # Single LLM call for main story
        response = self._call_llm(instruction, articles)

        # Check if all articles were filtered as noise
        filtered_articles = get_filtered_articles(articles, response, self.config)
        if not filtered_articles:
            return {
                **self._empty_story(),
                "noise_article_ids": [a["id"] for a in articles],
            }

        # Parse response into story structure
        story = parse_response(response, self.config, articles)

        # Generate substories if enabled
        if self.config.generate_substories:
            subgroups = get_subgroups(response, self.config)
            if subgroups:
                story["sub_stories"] = [
                    self._generate_substory(subgroup, filtered_articles)
                    for subgroup in subgroups
                ]

        return story

    def _call_llm(self, instruction: str, articles: list[dict]) -> dict:
        """
        Make a single LLM call with the given instruction and articles.

        Args:
            instruction: Combined system instruction
            articles: Articles to process

        Returns:
            Parsed JSON response from LLM
        """
        # Prepare article data for the LLM
        articles_for_llm = [
            {
                "id": article["id"],
                "title": article["title"],
                "summary": article["summary"],
                "text": article["text"],
                "source": article["source"],
                "published_at": article["published_at"],
            }
            for article in articles
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": json.dumps(articles_for_llm)},
            ],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    def _generate_substory(self, subgroup: dict, all_articles: list[dict]) -> dict:
        """
        Generate a substory for a sub-group of articles.

        Args:
            subgroup: Dict with 'theme' and 'article_ids'
            all_articles: Full list of filtered articles

        Returns:
            Substory dict with title, summary, article_ids
        """
        article_ids = set(subgroup.get("article_ids", []))
        subgroup_articles = [a for a in all_articles if a["id"] in article_ids]

        if not subgroup_articles:
            return {
                "title": subgroup.get("theme", ""),
                "summary": "",
                "article_ids": [],
            }

        # Use unified call for substory with title + summary only
        substory_config = CronkiteConfig(
            filter_noise=False,
            group_articles=False,
            generate_title=True,
            generate_summary=True,
            generate_key_points=False,
            extract_quotes=False,
            generate_substories=False,
        )

        instruction = build_instruction(substory_config)
        response = self._call_llm(instruction, subgroup_articles)

        return {
            "title": response.get("title", subgroup.get("theme", "")),
            "summary": response.get("summary", ""),
            "article_ids": list(article_ids),
        }

    def _empty_story(self) -> dict:
        """Return an empty story structure."""
        return {
            "title": "",
            "summary": "",
            "key_points": [],
            "quotes": [],
            "location": None,
            "sub_stories": [],
            "article_ids": [],
            "noise_article_ids": [],
        }
