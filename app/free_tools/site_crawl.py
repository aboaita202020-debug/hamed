"""Free-first, local website crawler for Hamed.

Uses only Python standard-library modules. It respects robots.txt, stays on the
same host, applies a small request delay, and returns evidence-backed findings.
Use only on sites you own or are authorized to audit.
"""
from __future__ import annotations

from collections import deque
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag, urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
import ssl
import time


class _PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.description = ""
        self.h1 = 0
        self.links: list[str] = []
        self.images_without_alt = 0
        self._title = False
        self._in_meta = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == "title":
            self._title = True
        elif tag.lower() == "meta" and attrs.get("name", "").lower() == "description":
            self.description = attrs.get("content", "").strip()
        elif tag.lower() == "h1":
            self.h1 += 1
        elif tag.lower() == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        elif tag.lower() == "img" and not attrs.get("alt", "").strip():
            self.images_without_alt += 1

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._title = False
            self.title = " ".join(self._title_parts).strip()

    def handle_data(self, data):
        if self._title:
            self._title_parts.append(data.strip())


def _fetch(url: str, timeout: int = 15) -> tuple[int, str]:
    req = Request(url, headers={"User-Agent": "HamedAI-FreeAudit/1.0"})
    with urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
        charset = r.headers.get_content_charset() or "utf-8"
        return r.status, r.read(2_000_000).decode(charset, errors="replace")


def crawl_site(seed_url: str, max_pages: int = 25, delay: float = 0.5) -> dict:
    seed = seed_url if seed_url.startswith(("http://", "https://")) else "https://" + seed_url
    parsed = urlparse(seed)
    host = parsed.netloc.lower()

    robots = RobotFileParser()
    robots.set_url(f"{parsed.scheme}://{host}/robots.txt")
    try:
        robots.read()
        robots_ok = True
    except Exception:
        robots_ok = False

    queue = deque([seed])
    seen: set[str] = set()
    pages = []
    findings = []

    while queue and len(pages) < max_pages:
        url = urldefrag(queue.popleft())[0]
        p = urlparse(url)
        if p.netloc.lower() != host or url in seen:
            continue
        seen.add(url)
        if robots_ok and not robots.can_fetch("HamedAI-FreeAudit/1.0", url):
            findings.append({"url": url, "severity": "info", "code": "robots_block", "evidence": "robots.txt disallows this URL"})
            continue
        try:
            status, html = _fetch(url)
        except Exception as exc:
            findings.append({"url": url, "severity": "warning", "code": "fetch_failed", "evidence": str(exc)[:240]})
            continue
        parser = _PageParser()
        parser.feed(html)
        page = {"url": url, "status": status, "title": parser.title, "description": parser.description,
                "h1_count": parser.h1, "images_without_alt": parser.images_without_alt}
        pages.append(page)
        if status >= 400:
            findings.append({"url": url, "severity": "error", "code": "http_error", "evidence": f"HTTP {status}"})
        if not parser.title:
            findings.append({"url": url, "severity": "warning", "code": "missing_title", "evidence": "No <title> element or title text was found"})
        if not parser.description:
            findings.append({"url": url, "severity": "warning", "code": "missing_meta_description", "evidence": "No meta description was found"})
        if parser.h1 == 0:
            findings.append({"url": url, "severity": "warning", "code": "missing_h1", "evidence": "No <h1> element was found"})
        if parser.images_without_alt:
            findings.append({"url": url, "severity": "info", "code": "images_missing_alt", "evidence": f"{parser.images_without_alt} image(s) have no alt text"})

        for href in parser.links:
            child = urldefrag(urljoin(url, href))[0]
            cp = urlparse(child)
            if cp.scheme in ("http", "https") and cp.netloc.lower() == host and child not in seen:
                queue.append(child)
        time.sleep(max(0.0, delay))

    return {"seed_url": seed, "pages": pages, "findings": findings,
            "pages_crawled": len(pages), "robots_checked": robots_ok}
