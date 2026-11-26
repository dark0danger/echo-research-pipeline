from .planner import plan
from .ranker import rank
from .report import build
from .sources import SOURCES


def run(topic: str, sources=("wikipedia", "arxiv"), top: int = 6) -> str:
    queries = plan(topic)
    items = []
    for q in queries:
        for name in sources:
            try:
                items += SOURCES[name](q)
            except Exception as exc:
                print(f"warn: {name} failed for '{q}': {exc}")
    return build(topic, queries, rank(topic, items, top))
