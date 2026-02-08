#!/usr/bin/env python
"""
Test script for Cronkite story grouping.

Usage:
    python -m tests.test_group_stories <cluster_a> <cluster_b> [--model MODEL]

Examples:
    python -m tests.test_group_stories middle_east_conflict political_election
    python -m tests.test_group_stories middle_east_conflict turkey_earthquake --model gpt-4o-mini

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


def save_output(cluster_a: str, cluster_b: str, links: list[dict], model: str) -> Path:
    """Save grouping results to test output directory."""
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"group_{cluster_a}_{cluster_b}_{model}_{timestamp}.json"
    output_path = TEST_OUTPUT_DIR / output_filename

    output = {
        "cluster_a": cluster_a,
        "cluster_b": cluster_b,
        "model": model,
        "generated_at": datetime.now().isoformat(),
        "links": links,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Group stories from two test article clusters"
    )
    parser.add_argument(
        "cluster_a",
        type=str,
        nargs="?",
        help="Name of first cluster (without .json extension)",
    )
    parser.add_argument(
        "cluster_b",
        type=str,
        nargs="?",
        help="Name of second cluster (without .json extension)",
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

    if not args.cluster_a or not args.cluster_b:
        parser.error("two cluster names are required (use --list to see available)")

    print(f"Initializing Cronkite with model: {args.model}")
    cronkite = Cronkite(model=args.model)

    # Generate stories from each cluster
    groups = {}
    for name in [args.cluster_a, args.cluster_b]:
        print(f"\nLoading cluster: {name}")
        articles = load_cluster(name)
        print(f"Loaded {len(articles)} articles")

        print("Generating story...")
        story = cronkite.generate_story(articles)
        story["_cluster_name"] = name
        groups[name] = story
        print(f"Generated: {story.get('title', 'No title')}")

    group_a = [groups[args.cluster_a]]
    group_b = [groups[args.cluster_b]]

    # Group stories
    print(f"\nGrouping stories across {args.cluster_a} and {args.cluster_b}...")
    links = cronkite.group_stories(group_a, group_b)

    output_path = save_output(args.cluster_a, args.cluster_b, links, args.model)
    print(f"\nGrouping results saved to: {output_path}\n")

    # Print summary
    print("=" * 60)
    print("GROUPING RESULTS")
    print("=" * 60)

    if not links:
        print("\nNo matching stories found across the two groups.")
    else:
        for link in links:
            a_idx = link["group_a_index"]
            b_idx = link["group_b_index"]
            a_title = group_a[a_idx].get("title", "No title") if a_idx < len(group_a) else "?"
            b_title = group_b[b_idx].get("title", "No title") if b_idx < len(group_b) else "?"
            print(f"\n  [{args.cluster_a} #{a_idx}] {a_title}")
            print(f"  [{args.cluster_b} #{b_idx}] {b_title}")


if __name__ == "__main__":
    main()
