#!/usr/bin/env python
"""
Test script for Cronkite story classification.

Usage:
    python -m tests.test_classify_stories <cluster_names...> [--model MODEL]

Examples:
    python -m tests.test_classify_stories middle_east_conflict
    python -m tests.test_classify_stories middle_east_conflict tech_product_launch
    python -m tests.test_classify_stories --all --model gpt-4o-mini

Available clusters:
    Run with --list to see available clusters
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


def save_output(cluster_names: list[str], classified_stories: list[dict], model: str) -> Path:
    """Save classified stories to test output directory."""
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"classify_{'_'.join(cluster_names)}_{model}_{timestamp}.json"
    output_path = TEST_OUTPUT_DIR / output_filename

    output = {
        "cluster_names": cluster_names,
        "model": model,
        "generated_at": datetime.now().isoformat(),
        "classified_stories": classified_stories,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Classify stories from test article clusters"
    )
    parser.add_argument(
        "clusters",
        type=str,
        nargs="*",
        help="Names of clusters to process (without .json extension)",
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
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all available clusters",
    )

    args = parser.parse_args()

    if args.list:
        clusters = list_available_clusters()
        print("Available clusters:")
        for cluster in clusters:
            print(f"  - {cluster}")
        return

    cluster_names = args.clusters
    if args.all:
        cluster_names = list_available_clusters()

    if not cluster_names:
        parser.error("at least one cluster is required (use --list to see available, or --all)")

    print(f"Initializing Cronkite with model: {args.model}")
    cronkite = Cronkite(model=args.model)

    # Generate stories from each cluster
    stories = []
    for cluster_name in cluster_names:
        print(f"\nLoading cluster: {cluster_name}")
        articles = load_cluster(cluster_name)
        print(f"Loaded {len(articles)} articles")

        print("Generating story...")
        story = cronkite.generate_story(articles)
        story["_cluster_name"] = cluster_name
        stories.append(story)
        print(f"Generated: {story.get('title', 'No title')}")

    # Classify all stories
    print(f"\nClassifying {len(stories)} stories...")
    classified_stories = cronkite.classify_stories(stories)

    output_path = save_output(cluster_names, classified_stories, args.model)
    print(f"\nClassified stories saved to: {output_path}\n")

    # Print summary
    print("=" * 60)
    print("CLASSIFICATION RESULTS")
    print("=" * 60)
    for story in classified_stories:
        cluster = story.get("_cluster_name", "unknown")
        title = story.get("title", "No title")
        topics = story.get("topics", [])
        print(f"\n[{cluster}]")
        print(f"Title: {title}")
        print(f"Topics: {', '.join(topics) if topics else 'None'}")


if __name__ == "__main__":
    main()
