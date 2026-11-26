"""Dedupe and rank evidence by keyword overlap with the topic."""
import re

from .sources import Evidence

STOP = {"the", "a", "an", "of", "and", "in", "on", "for", "to", "is", "are", "with"}


def tokens(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP}


def score(topic: str, ev: Evidence) -> float:
    t = tokens(topic)
    if not t:
        return 0.0
    body = tokens(ev.title + " " + ev.text)
    title = tokens(ev.title)
    return len(t & body) / len(t) + 0.5 * len(t & title) / len(t)


def rank(topic: str, items: list[Evidence], top: int = 6) -> list[Evidence]:
    seen, unique = set(), []
    for ev in items:
        key = ev.url or ev.title
        if key not in seen:
            seen.add(key)
            unique.append(ev)
    return sorted(unique, key=lambda e: score(topic, e), reverse=True)[:top]
