"""Dependency-light website audit using only Python standard library.

This is intentionally evidence-first: it reports observable page-level signals and
never invents a defect. It is a free-first baseline, not a replacement for a full
browser/SEO crawler.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen


@dataclass
class Finding:
    key: str
    severity: str
    evidence: str
    commercial_impact: str
    suggested_service: str


class _PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.h1_count = 0
        self.img_count = 0
        self.images_without_alt = 0
        self.links = 0
        self.forms = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta" and attrs_dict.get("name", "").lower() == "description":
            self.meta_description = attrs_dict.get("content") or ""
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img":
            self.img_count += 1
            if not (attrs_dict.get("alt") or "").strip():
                self.images_without_alt += 1
        elif tag == "a":
            self.links += 1
        elif tag == "form":
            self.forms += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()


def fetch_page(url: str, timeout: int = 12) -> tuple[str, str, int]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must be an absolute http(s) URL")
    request = Request(url, headers={"User-Agent": "Hamed-FreeAudit/1.0"})
    with urlopen(request, timeout=timeout) as response:
        body = response.read(2_000_000).decode("utf-8", errors="replace")
        return response.geturl(), response.headers.get_content_type(), response.status


def audit_url(url: str) -> dict:
    final_url, content_type, status = fetch_page(url)
    findings: list[Finding] = []
    parser = _PageParser()
    if "html" not in content_type:
        return {"url": final_url, "status": status, "content_type": content_type, "findings": []}

    # Re-fetch is avoided by keeping the scanner simple; the caller can pass cached HTML
    # to audit_html for bulk crawling.
    request = Request(final_url, headers={"User-Agent": "Hamed-FreeAudit/1.0"})
    with urlopen(request, timeout=12) as response:
        html = response.read(2_000_000).decode("utf-8", errors="replace")
    parser.feed(html)

    if not parser.title:
        findings.append(Finding("missing_title", "high", "No <title> text was observed.", "Weak search-result messaging and browser context.", "SEO/content optimization"))
    if not parser.meta_description:
        findings.append(Finding("missing_meta_description", "medium", "No meta description was observed.", "Less control over search-result presentation.", "SEO optimization"))
    if parser.h1_count == 0:
        findings.append(Finding("missing_h1", "medium", "No H1 heading was observed.", "Weaker page hierarchy and message clarity.", "Landing-page optimization"))
    if parser.h1_count > 1:
        findings.append(Finding("multiple_h1", "low", f"Observed {parser.h1_count} H1 headings.", "May reduce clarity of the primary page message.", "UX/content optimization"))
    if parser.img_count and parser.images_without_alt:
        findings.append(Finding("image_alt_gaps", "low", f"{parser.images_without_alt}/{parser.img_count} images lack alt text.", "Accessibility and image-search discoverability can be reduced.", "SEO/accessibility optimization"))
    if parser.forms == 0 and parser.links == 0:
        findings.append(Finding("weak_conversion_path", "medium", "No forms or links were observed on the page.", "Visitors may have no obvious next action.", "Conversion optimization"))

    return {
        "url": final_url,
        "status": status,
        "content_type": content_type,
        "signals": asdict(parser),
        "findings": [asdict(f) for f in findings],
    }
