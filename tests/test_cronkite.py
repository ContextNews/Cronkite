#!/usr/bin/env python
"""
Test script for Cronkite story generation.

Usage:
    python -m tests.test_cronkite <cluster_name> [--model MODEL]

Examples:
    python -m tests.test_cronkite middle_east_conflict
    python -m tests.test_cronkite tech_product_launch --model gpt-4o-mini
    python -m tests.test_cronkite political_election

Available clusters:
    - middle_east_conflict
    - tech_product_launch
    - political_election
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from cronkite import Cronkite


TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"


def list_available_clusters() -> list[str]:
    """List all available test clusters."""
    return [f.stem for f in TEST_DATA_DIR.glob("*.json")]


def load_cluster(cluster_name: str) -> list[dict]:
    """Load articles from a test cluster file."""
    cluster_path = TEST_DATA_DIR / f"{cluster_name}.json"
    if not cluster_path.exists():
        available = list_available_clusters()
        raise FileNotFoundError(
            f"Cluster '{cluster_name}' not found. "
            f"Available clusters: {', '.join(available)}"
        )

    with open(cluster_path, "r") as f:
        return json.load(f)


def save_output(cluster_name: str, story: dict, model: str) -> Path:
    """Save generated story to test output directory."""
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{cluster_name}_{model}_{timestamp}.json"
    output_path = TEST_OUTPUT_DIR / output_filename

    output = {
        "cluster_name": cluster_name,
        "model": model,
        "generated_at": datetime.now().isoformat(),
        "story": story,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate a story from a test article cluster"
    )
    parser.add_argument(
        "cluster",
        type=str,
        nargs="?",
        help="Name of the cluster to process (without .json extension)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available clusters and exit",
    )

    args = parser.parse_args()

    if args.list:
        clusters = list_available_clusters()
        print("Available clusters:")
        for cluster in clusters:
            print(f"  - {cluster}")
        return

    if not args.cluster:
        parser.error("cluster is required (use --list to see available clusters)")

    print(f"Loading cluster: {args.cluster}")
    articles = load_cluster(args.cluster)
    print(f"Loaded {len(articles)} articles")

    print(f"Initializing Cronkite with model: {args.model}")
    cronkite = Cronkite(model=args.model)

    print("Generating story...")
    story = cronkite.generate_story(articles)

    output_path = save_output(args.cluster, story, args.model)
    print(f"Story saved to: {output_path}")

    print("\n" + "=" * 60)
    print("GENERATED STORY")
    print("=" * 60)
    print(f"\nTitle: {story['title']}")
    print(f"\nSummary:\n{story['summary']}")
    print(f"\nQuotes ({len(story['quotes'])}):")
    for quote in story['quotes']:
        speaker = quote.get('speaker_name') or quote.get('speaker_org') or 'Unknown'
        print(f"  - \"{quote['text'][:100]}...\" - {speaker}")
    print(f"\nSub-stories ({len(story['sub_stories'])}):")
    for sub in story['sub_stories']:
        print(f"  - {sub['title']}")
    print(f"\nArticles used: {len(story['article_ids'])}")
    print(f"Noise filtered: {len(story['noise_article_ids'])}")


if __name__ == "__main__":
    main()
