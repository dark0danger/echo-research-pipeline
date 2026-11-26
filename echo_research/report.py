"""Build a markdown report. Optional LLM summary via any OpenAI-compatible API."""
import json
import os
import urllib.request

from .sources import Evidence


def first_sentences(text: str, n: int = 2) -> str:
    parts = text.replace("\n", " ").split(". ")
    s = ". ".join(parts[:n]).strip()
    return s if s.endswith(".") else s + "."


def llm_summary(topic: str, items: list[Evidence]) -> str | None:
    key = os.environ.get("LLM_API_KEY")
    if not key:
        return None
    base = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    ctx = "\n\n".join(f"[{i+1}] {e.title}: {e.text[:600]}" for i, e in enumerate(items))
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": "Summarize only from the numbered sources and cite them like [1]."},
        {"role": "user", "content": f"Topic: {topic}\n\n{ctx}"}]}).encode()
    req = urllib.request.Request(f"{base}/chat/completions", data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def build(topic: str, queries: list[str], items: list[Evidence]) -> str:
    lines = [f"# Research report: {topic}", "", "## Search plan", ""]
    lines += [f"- {q}" for q in queries]
    lines += ["", "## Summary", ""]
    summary = None
    try:
        summary = llm_summary(topic, items)
    except Exception as exc:  # network or API failure: fall back
        lines.append(f"_LLM summary unavailable ({type(exc).__name__}); using extractive summary._\n")
    if summary:
        lines.append(summary)
    else:
        lines += [f"- {first_sentences(e.text)} [{i+1}]" for i, e in enumerate(items) if e.text]
    lines += ["", "## Sources", ""]
    lines += [f"{i+1}. [{e.title}]({e.url}) ({e.source})" for i, e in enumerate(items)]
    return "\n".join(lines) + "\n"
