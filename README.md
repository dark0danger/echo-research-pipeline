# Echo Research Pipeline

Echo INC milestone#2 session3

A small research agent that turns a topic into a cited markdown report. It runs as a fixed pipeline: plan, gather, rank, report. It uses only the Python standard library, so there is nothing to install to run it.

## Pipeline

```text
topic -> planner (sub-queries) -> sources (Wikipedia, arXiv) -> ranker (dedupe + relevance) -> report
```

- `planner.py`: builds focused sub-queries from the topic.
- `sources.py`: Wikipedia and arXiv fetchers returning `Evidence` records.
- `ranker.py`: removes duplicates and scores by keyword overlap with the topic.
- `report.py`: writes the report. With `LLM_API_KEY` set it asks any OpenAI-compatible model for a cited summary. Without it, it falls back to an extractive summary.

## Run

```bash
python -m echo_research "solid state batteries" --out report.md
```

Optional LLM summary: copy `.env.example`, export the variables, then run the same command.

## Test

```bash
pip install pytest && pytest -q
```
