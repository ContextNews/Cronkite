# Cronkite

An LLM-powered news aggregation engine that synthesizes coherent stories from clusters of related articles.

## Overview

Cronkite takes a cluster of news articles about the same event and produces a unified story with:
- A short, neutral event label (e.g., "Cairo Ceasefire Negotiations")
- A condensed single-paragraph summary
- Key points (3-6 bullet points)
- Extracted quotes with speaker attribution
- Story location (country, region, city)
- Optional sub-stories for distinct developments within the event

## How It Works

```
Articles In → Filter Noise → Group Sub-clusters → Generate Story → JSON Out
```

**Pipeline (single unified LLM call):**

1. **Filter Noise** — Removes articles that don't belong (off-topic, generic roundups)
2. **Group Articles** — Identifies meaningful sub-clusters (e.g., separate incidents)
3. **Generate Title** — Creates a short, neutral event label (2-6 words)
4. **Generate Summary** — Synthesizes a condensed single-paragraph summary (150-200 words)
5. **Generate Key Points** — Extracts 3-6 key facts from the articles
6. **Extract Quotes** — Pulls notable quotes with speaker metadata
7. **Resolve Location** — Determines the primary geographic location
8. **Generate Sub-stories** — Creates titles and summaries for each sub-cluster

## Installation

```bash
poetry install
```

Requires `OPENAI_API_KEY` in environment or `.env` file.

## Usage

```python
from cronkite import Cronkite, CronkiteConfig

# Default: all actions enabled
cronkite = Cronkite(model="gpt-4o")
story = cronkite.generate_story(articles)

# Custom config: disable specific actions
config = CronkiteConfig(
    filter_noise=True,
    group_articles=True,
    generate_title=True,
    generate_summary=True,
    generate_key_points=True,
    extract_quotes=False,      # Disable quotes
    resolve_location=False,    # Disable location
    generate_substories=False, # Disable sub-stories
)
cronkite = Cronkite(model="gpt-4o-mini", config=config)
story = cronkite.generate_story(articles)
```

## Input Schema

```python
articles = [
    {
        "id": "unique-id",
        "title": "Article Headline",
        "summary": "Brief lede or summary",
        "text": "Full article text...",
        "published_at": "2024-03-15T09:30:00Z",
        "source": "Reuters"
    }
]
```

## Output Schema

```python
{
    "title": "Event Label",  # e.g., "Cairo Ceasefire Negotiations"
    "summary": "Condensed single-paragraph summary...",
    "key_points": [
        "Key fact or development 1",
        "Key fact or development 2",
        "Key fact or development 3"
    ],
    "quotes": [
        {
            "text": "The exact quote",
            "speaker_name": "John Smith",
            "speaker_title": "Secretary of State",
            "speaker_org": "State Department",
            "speaker_nation": "USA",  # ISO3
            "article_id": "source-article-id"
        }
    ],
    "location": {
        "country": "EGY",       # ISO3 code
        "region": "Cairo",      # State/province/region
        "city": "Cairo"         # City/town (null if unknown)
    },
    "sub_stories": [
        {
            "title": "Sub-event Headline",
            "summary": "Focused summary...",
            "article_ids": ["id-1", "id-2"]
        }
    ],
    "article_ids": ["ids", "of", "articles", "used"],
    "noise_article_ids": ["ids", "filtered", "out"]
}
```

## Project Structure

```
src/cronkite/
├── cronkite.py              # Main orchestrator
├── config.py                # CronkiteConfig dataclass
├── instruction_builder.py   # Combines instructions based on config
├── response_parser.py       # Parses LLM response
└── instructions/
    └── generate_story/      # Modular instruction components
        ├── generate_story_base.py
        ├── filter_noise.py
        ├── group_articles.py
        ├── generate_title.py
        ├── generate_summary.py
        ├── generate_key_points.py
        ├── extract_quotes.py
        └── resolve_location.py
```

## Testing

```bash
# List available test clusters
poetry run python -m tests.test_cronkite --list

# Run on a test cluster
poetry run python -m tests.test_cronkite middle_east_conflict
poetry run python -m tests.test_cronkite tech_product_launch --model gpt-4o-mini
```

## Design Principles

- **Neutrality** — Headlines and summaries are factual, not sensational
- **Source Synthesis** — Information is cross-referenced across articles
- **Graceful Degradation** — Handles edge cases (single articles, all noise, no quotes)
- **Configurable** — Model and pipeline actions configurable at instantiation
- **Token Efficient** — Single unified LLM call instead of multiple separate calls

## License

MIT
