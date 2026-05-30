#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from typing import Any
from urllib import parse, request
from urllib.error import HTTPError, URLError
import xml.etree.ElementTree as ET


USER_AGENT = "ai-paper-digest-skill/1.0"
ARXIV_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "stat.ML"]
AI_KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "large language model",
    "computer vision",
    "natural language processing",
    "reinforcement learning",
]
VENUE_HINTS = [
    "icml",
    "neurips",
    "nips",
    "iclr",
    "cvpr",
    "iccv",
    "eccv",
    "aaai",
    "ijcai",
    "kdd",
    "icdm",
    "aistats",
    "colt",
    "tpami",
    "tkde",
    "jmlr",
    "tmlr",
]


@dataclass
class Paper:
    title: str
    paper_url: str
    source_name: str
    venue: str
    published_or_seen_date: str
    authors: list[str]
    abstract: str
    method_keywords: list[str]
    reason_to_watch: str
    score: float


def fetch_text(url: str, accept: str | None = None) -> str:
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    req = request.Request(url, headers=headers)
    with request.urlopen(req, timeout=25) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_json(url: str) -> dict[str, Any]:
    return json.loads(fetch_text(url, accept="application/json"))


def clean_text(text: str, limit: int = 1000) -> str:
    normalized = re.sub(r"\s+", " ", text or "").strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"


def infer_venue(text: str, source_name: str) -> str:
    lowered = f"{text} {source_name}".lower()
    for hint in VENUE_HINTS:
        if hint in lowered:
            return hint.upper() if hint != "nips" else "NeurIPS"
    return ""


def extract_method_keywords(text: str) -> list[str]:
    lowered = text.lower()
    candidates = [
        "transformer",
        "diffusion",
        "retrieval",
        "reasoning",
        "agent",
        "multimodal",
        "reinforcement learning",
        "alignment",
        "vision-language",
        "graph neural network",
        "contrastive learning",
        "optimization",
        "generalization",
    ]
    return [keyword for keyword in candidates if keyword in lowered][:5]


def choose_reason(title: str, abstract: str, venue: str) -> str:
    lowered = f"{title} {abstract}".lower()
    if venue:
        return f"与 {venue} 相关，适合作为该方向的近期代表性论文。"
    if "llm" in lowered or "language model" in lowered:
        return "与大模型相关，通常具有较高关注度。"
    if "diffusion" in lowered or "multimodal" in lowered:
        return "涉及当前活跃的生成式或多模态方向。"
    if "reinforcement learning" in lowered or "agent" in lowered:
        return "涉及智能体或强化学习，适合持续跟踪。"
    return "主题与近期 AI 研究热点接近，值得做快速筛读。"


def fetch_arxiv(now: datetime, days: int) -> list[Paper]:
    query = " OR ".join(f"cat:{category}" for category in ARXIV_CATEGORIES)
    url = (
        "https://export.arxiv.org/api/query?"
        f"search_query={parse.quote(query)}&sortBy=submittedDate&sortOrder=descending&max_results=40"
    )
    root = ET.fromstring(fetch_text(url))
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers: list[Paper] = []
    cutoff = now - timedelta(days=days)
    for entry in root.findall("atom:entry", ns):
        title = clean_text(entry.findtext("atom:title", default="", namespaces=ns), 220)
        abstract = clean_text(entry.findtext("atom:summary", default="", namespaces=ns))
        published_raw = entry.findtext("atom:published", default="", namespaces=ns)
        published = datetime.fromisoformat(published_raw.replace("Z", "+00:00")).astimezone(UTC)
        if published < cutoff:
            continue
        authors = [
            clean_text(author.findtext("atom:name", default="", namespaces=ns), 80)
            for author in entry.findall("atom:author", ns)
        ]
        link = ""
        for item in entry.findall("atom:link", ns):
            if item.attrib.get("rel") == "alternate":
                link = item.attrib.get("href", "")
                break
        venue = infer_venue(title + " " + abstract, "arXiv")
        papers.append(
            Paper(
                title=title,
                paper_url=link,
                source_name="arXiv",
                venue=venue,
                published_or_seen_date=published.date().isoformat(),
                authors=authors[:6],
                abstract=abstract,
                method_keywords=extract_method_keywords(title + " " + abstract),
                reason_to_watch=choose_reason(title, abstract, venue),
                score=12 + max(0, (cutoff - published).days * -1),
            )
        )
    return papers


def invert_abstract(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, offsets in index.items():
        for offset in offsets:
            positions.append((offset, word))
    return clean_text(" ".join(word for _, word in sorted(positions)))


def fetch_openalex(now: datetime, days: int) -> list[Paper]:
    since = (now - timedelta(days=days)).date().isoformat()
    until = now.date().isoformat()
    filters = ",".join(
        [
            f"from_publication_date:{since}",
            f"to_publication_date:{until}",
            "type:article",
            "has_abstract:true",
            "locations.source.type:journal",
        ]
    )
    fields = ",".join(
        [
            "id",
            "title",
            "publication_date",
            "authorships",
            "best_oa_location",
            "primary_location",
            "cited_by_count",
            "abstract_inverted_index",
            "concepts",
        ]
    )
    url = (
        "https://api.openalex.org/works?"
        f"filter={parse.quote(filters)}&sort=publication_date:desc&per-page=50&select={fields}"
    )
    payload = fetch_json(url)
    papers: list[Paper] = []
    for item in payload.get("results", []):
        title = clean_text(item.get("title", ""), 220)
        abstract = invert_abstract(item.get("abstract_inverted_index"))
        joined = f"{title} {abstract}".lower()
        if not any(keyword in joined for keyword in AI_KEYWORDS):
            continue
        location = item.get("best_oa_location") or item.get("primary_location") or {}
        source = (location.get("source") or {}).get("display_name") or "Journal"
        venue = infer_venue(title + " " + abstract, source)
        cited_by = item.get("cited_by_count", 0) or 0
        authors = [
            clean_text((authorship.get("author") or {}).get("display_name", ""), 80)
            for authorship in item.get("authorships", [])
            if (authorship.get("author") or {}).get("display_name")
        ]
        papers.append(
            Paper(
                title=title,
                paper_url=location.get("landing_page_url") or item.get("id", ""),
                source_name=source,
                venue=venue,
                published_or_seen_date=item.get("publication_date", ""),
                authors=authors[:6],
                abstract=abstract,
                method_keywords=extract_method_keywords(title + " " + abstract),
                reason_to_watch=choose_reason(title, abstract, venue),
                score=8 + min(cited_by / 10, 6),
            )
        )
    return papers


class HuggingFacePaperParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._current_href = ""
        self._capture = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attr_map = dict(attrs)
        href = attr_map.get("href") or ""
        if href.startswith("/papers/"):
            self._current_href = "https://huggingface.co" + href
            self._capture = True
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._capture:
            title = clean_text("".join(self._buffer), 220)
            if title and len(title) > 20:
                self.links.append((title, self._current_href))
            self._capture = False
            self._current_href = ""
            self._buffer = []


def fetch_huggingface(now: datetime) -> list[Paper]:
    parser = HuggingFacePaperParser()
    parser.feed(fetch_text("https://huggingface.co/papers"))
    papers: list[Paper] = []
    seen: set[str] = set()
    for title, href in parser.links:
        lowered = title.lower()
        if title in seen:
            continue
        seen.add(title)
        venue = infer_venue(title, "Hugging Face Papers")
        papers.append(
            Paper(
                title=title,
                paper_url=href,
                source_name="Hugging Face Papers",
                venue=venue,
                published_or_seen_date=now.date().isoformat(),
                authors=[],
                abstract="",
                method_keywords=extract_method_keywords(lowered),
                reason_to_watch=choose_reason(title, "", venue),
                score=7 + (2 if venue else 0),
            )
        )
        if len(papers) >= 20:
            break
    return papers


def dedupe_and_sort(papers: list[Paper], limit: int) -> list[Paper]:
    unique: dict[str, Paper] = {}
    for paper in sorted(papers, key=lambda item: item.score, reverse=True):
        key = paper.title.lower()
        if key not in unique:
            unique[key] = paper
    return list(unique.values())[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a recent AI paper digest.")
    parser.add_argument("--days", type=int, default=3, help="Lookback window for recent papers.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum papers to output.")
    args = parser.parse_args()

    now = datetime.now(UTC)
    papers: list[Paper] = []
    warnings: list[str] = []

    for name, fetcher in [
        ("arXiv", lambda: fetch_arxiv(now, args.days)),
        ("OpenAlex", lambda: fetch_openalex(now, args.days)),
        ("Hugging Face Papers", lambda: fetch_huggingface(now)),
    ]:
        try:
            papers.extend(fetcher())
        except (HTTPError, URLError, TimeoutError, ET.ParseError, ValueError) as exc:
            warnings.append(f"{name} failed: {exc}")

    output = {
        "generated_at": now.isoformat(timespec="seconds"),
        "lookback_days": args.days,
        "papers": [asdict(paper) for paper in dedupe_and_sort(papers, args.limit)],
        "warnings": warnings,
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
