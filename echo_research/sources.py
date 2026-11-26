"""Evidence sources. Each returns a list of Evidence. Uses only the standard library."""
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass

UA = {"User-Agent": "echo-research/0.1 (educational project)"}


@dataclass
class Evidence:
    source: str
    title: str
    url: str
    text: str


def _get(url: str, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def wikipedia(query: str, limit: int = 3) -> list[Evidence]:
    params = urllib.parse.urlencode({
        "action": "query", "generator": "search", "gsrsearch": query,
        "gsrlimit": limit, "prop": "extracts", "exintro": 1,
        "explaintext": 1, "format": "json"})
    data = json.loads(_get(f"https://en.wikipedia.org/w/api.php?{params}"))
    pages = data.get("query", {}).get("pages", {}).values()
    return [Evidence("wikipedia", p["title"],
                     "https://en.wikipedia.org/?curid=%s" % p["pageid"],
                     p.get("extract", "")[:1500]) for p in pages]


def arxiv(query: str, limit: int = 3) -> list[Evidence]:
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}", "max_results": limit})
    root = ET.fromstring(_get(f"http://export.arxiv.org/api/query?{params}"))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in root.findall("a:entry", ns):
        out.append(Evidence(
            "arxiv",
            " ".join(e.findtext("a:title", "", ns).split()),
            e.findtext("a:id", "", ns),
            " ".join(e.findtext("a:summary", "", ns).split())[:1500]))
    return out


SOURCES = {"wikipedia": wikipedia, "arxiv": arxiv}
