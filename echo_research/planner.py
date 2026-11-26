"""Turn a topic into sub-queries. Rule-based, so it works offline and is testable."""

ANGLES = ["{t}", "{t} overview", "{t} recent advances", "{t} limitations challenges"]


def plan(topic: str, n: int = 4) -> list[str]:
    topic = " ".join(topic.split())
    if not topic:
        raise ValueError("topic must not be empty")
    return [a.format(t=topic) for a in ANGLES[:n]]
