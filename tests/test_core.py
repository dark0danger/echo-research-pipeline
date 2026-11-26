import pytest

from echo_research.planner import plan
from echo_research.ranker import rank
from echo_research.report import build
from echo_research.sources import Evidence


def test_plan():
    assert plan("solid state batteries")[0] == "solid state batteries"
    with pytest.raises(ValueError):
        plan("  ")


def test_rank_dedupes_and_orders():
    a = Evidence("x", "Solid state batteries", "u1", "solid state batteries store energy")
    b = Evidence("x", "Cooking", "u2", "pasta")
    c = Evidence("x", "dup", "u1", "solid")
    out = rank("solid state batteries", [b, a, c])
    assert out[0] is a and len(out) == 2


def test_report_has_sources(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    ev = [Evidence("wikipedia", "T", "http://t", "One. Two. Three.")]
    md = build("topic", ["q"], ev)
    assert "## Sources" in md and "[T](http://t)" in md
