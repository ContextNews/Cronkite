from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

from cronkite.actions import (
    filter_noise,
    group_articles,
    generate_title,
    generate_summary,
    extract_quotes,
)


class Cronkite:
    """
    LLM-powered agent that generates cohesive news stories from article clusters.
    """

    def __init__(self, model: str = "gpt-4o"):
        """
        Initialize Cronkite with a configurable OpenAI model.

        Args:
            model: OpenAI model identifier (e.g., "gpt-4o", "gpt-4o-mini")
        """
        self.model = model
        self.client = OpenAI()

    def generate_story(self, articles: list[dict]) -> dict:
        """
        Process articles through the full pipeline and return a story.

        Args:
            articles: List of article dicts with id, title, summary, text,
                      published_at, source

        Returns:
            Story dict with title, summary, quotes, sub_stories,
            article_ids, noise_article_ids
        """
        if not articles:
            return {
                "title": "",
                "summary": "",
                "quotes": [],
                "sub_stories": [],
                "article_ids": [],
                "noise_article_ids": [],
            }

        # Step 1: Filter noise
        filtered_articles, noise_ids = filter_noise(
            articles, self.client, self.model
        )

        if not filtered_articles:
            return {
                "title": "",
                "summary": "",
                "quotes": [],
                "sub_stories": [],
                "article_ids": [],
                "noise_article_ids": noise_ids,
            }

        # Step 2: Group articles into sub-clusters
        subgroups = group_articles(filtered_articles, self.client, self.model)

        # Step 3: Generate main story title
        title = generate_title(filtered_articles, self.client, self.model)

        # Step 4: Generate main story summary
        summary = generate_summary(filtered_articles, self.client, self.model)

        # Step 5: Extract quotes
        quotes = extract_quotes(filtered_articles, self.client, self.model)

        # Step 6: Generate substories for each sub-group
        sub_stories = []
        for subgroup in subgroups:
            sub_stories.append(self._generate_substory(subgroup, filtered_articles))

        return {
            "title": title,
            "summary": summary,
            "quotes": quotes,
            "sub_stories": sub_stories,
            "article_ids": [a["id"] for a in filtered_articles],
            "noise_article_ids": noise_ids,
        }

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

        title = generate_title(subgroup_articles, self.client, self.model)
        summary = generate_summary(subgroup_articles, self.client, self.model)

        return {
            "title": title,
            "summary": summary,
            "article_ids": list(article_ids),
        }
