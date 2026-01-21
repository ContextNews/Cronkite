# Cronkite

An LLM-powered news aggregation engine that synthesizes coherent stories from clusters of related articles.

## Overview

Cronkite takes a cluster of news articles about the same event and produces a unified story with:
- A short, neutral event label (e.g., "Cairo Ceasefire Negotiations")
- A condensed single-paragraph summary
- Extracted quotes with speaker attribution
- Optional sub-stories for distinct developments within the event

## How It Works

```
Articles In → Filter Noise → Group Sub-clusters → Generate Story → JSON Out
```

**Pipeline:**

1. **Filter Noise** — Removes articles that don't belong (off-topic, generic roundups like "Today's Headlines")
2. **Group Articles** — Identifies meaningful sub-clusters (e.g., separate incidents within a conflict)
3. **Generate Title** — Creates a short, neutral event label (2-6 words)
4. **Generate Summary** — Synthesizes a condensed single-paragraph summary (150-200 words)
5. **Extract Quotes** — Pulls notable quotes with speaker metadata
6. **Generate Sub-stories** — Creates titles and summaries for each sub-cluster

## Installation

```bash
poetry install
```

Requires `OPENAI_API_KEY` in environment or `.env` file.

## Usage

```python
from cronkite import Cronkite

cronkite = Cronkite(model="gpt-4o")  # or "gpt-4o-mini"

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
├── actions/                 # Pipeline steps
│   ├── filter_noise.py
│   ├── group_articles.py
│   ├── generate_title.py
│   ├── generate_summary.py
│   └── extract_quotes.py
└── instructions/            # LLM prompts for each action
    ├── filter_noise.py
    ├── group_articles.py
    ├── generate_title.py
    ├── generate_summary.py
    └── extract_quotes.py
```

## Testing

```bash
# List available test clusters
poetry run python -m tests.test_cronkite --list

# Run on a test cluster
poetry run python -m tests.test_cronkite middle_east_conflict
poetry run python -m tests.test_cronkite tech_product_launch --model gpt-4o-mini
```

Test clusters include realistic article sets with intentional noise for validation.

## Design Principles

- **Neutrality** — Headlines and summaries are factual, not sensational
- **Source Synthesis** — Information is cross-referenced across articles
- **Graceful Degradation** — Handles edge cases (single articles, all noise, no quotes)
- **Configurable** — Model selection at instantiation

## License

MIT
