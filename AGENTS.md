# AGENTS.md

## Overview

Cronkite is a library (not a service) that turns a cluster of related news articles into a single synthesized story via the OpenAI API. It is consumed by other ContextNews repos — `news-pipeline` in particular — so treat the story dict shape as a published contract.

`README.md` documents the public API, input/output schemas, and topic list. This file covers how to work in the code.

## Commands

```bash
poetry install                                   # Python >=3.12, src layout
poetry run python -m tests.test_cronkite --list  # list test clusters
poetry run python -m tests.test_cronkite middle_east_conflict --model gpt-4o-mini
poetry run python -m tests.test_classify_stories --all
poetry run python -m tests.test_group_stories middle_east_conflict political_election
```

**`tests/` is not a pytest suite.** There is no test runner and no pytest dependency — the files are hand-run CLI scripts that make real, paid OpenAI calls and write JSON to `tests/test_output/`. `pytest` will collect nothing useful. Don't run them in a loop, and prefer `--model gpt-4o-mini` while iterating. `OPENAI_API_KEY` must be in the environment or `.env` (loaded by `cronkite.py` at import time).

## Architecture

Three public actions on `Cronkite`, each a thin wrapper over a function in `actions/`:

- `generate_story(articles)` — the main pipeline
- `classify_stories(stories)` — adds a `topics` field per story
- `group_stories(group_a, group_b)` — links stories across two groups that cover the same event (undocumented in README; used for cross-source dedupe)

`generate_story` is **one LLM call**, not one per step. `instruction_builder.build_instruction(config)` concatenates a base preamble plus the task text of each enabled component into a single system prompt with a generated output schema, and `response_parser` pulls the fields back out. Sub-stories are the exception: each subgroup costs one extra call, made with a cut-down `CronkiteConfig`.

Instruction components are plain dicts, not classes. Each lives in its own module under `instructions/<action>/` and must have `task`, `output_field`, `output_type`, `output_description`, `output_example`.

### Adding a pipeline step

Touch all five places or the field silently disappears:

1. New `*_COMPONENT` dict in `instructions/generate_story/<step>.py`
2. Export it from `instructions/generate_story/__init__.py`
3. Add a bool flag to `CronkiteConfig` (`config.py`)
4. Append it in `instruction_builder._get_enabled_components` — **order here is prompt order**
5. Add the field's default to `FIELD_DEFAULTS` and read it in `response_parser.parse_response`

## Conventions

- Prompt text lives in `instructions/`, never inline in `actions/` or `cronkite.py`. Tuning model behavior means editing a component's `task` string.
- Every config flag must degrade gracefully — a disabled action returns its `FIELD_DEFAULTS` value, so output keys are always present. Keep that invariant.
- Articles and stories are passed as plain dicts; there are no Pydantic models or dataclasses for them.
- Country codes are ISO3 (`"USA"`, `"EGY"`), timestamps ISO 8601 UTC.
- Neutral, non-sensational tone is a product requirement, not a style preference — keep it in any prompt you edit.
