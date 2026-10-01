from __future__ import annotations

import os
import time
from urllib.error import URLError
from html.parser import HTMLParser
from urllib.parse import parse_qs, quote_plus, unquote, urlparse
from urllib.request import Request, urlopen

from .web_source_registry import SOURCES
from .web_source_registry import catalog as source_catalog

FALLBACK_BUSINESS_URLS = [
    "https://www.asweshop.com/en",
    "https://www.ankh-eg.com/",
    "https://www.zoyafashioneg.com/",
    "https://www.gettoot.com/",
    "https://wujud.online/",
    "https://www.azola.store/",
    "https://trxtrwear.com/",
    "https://spottdegy.com/",
    "https://www.sohbaegypt.com/",
    "https://bygehad.com/",
]

DEFAULT_DISCOVERY_QUERIES = [
    "Egypt online store ecommerce",
    "Egypt ecommerce shop",
    "Middle East online store ecommerce",
    "Egypt restaurant online ordering",
    "Egypt business TikTok",
    "Egypt business Instagram",
    "Egypt business Facebook",
    "Egypt business YouTube",
    "Egypt business LinkedIn",
    "Egypt business X Twitter",
    "Egypt business Pinterest",
    "business looking for marketing agency",
    "small business needs website",
    "online store conversion problems",
    "new ecommerce business",
]

RETRYABLE_ERRNOS = {98, 99, 101, 104, 110, 111, 113}
MAX_RETRIES = 2
BACKOFF_SECONDS = 0.35


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, TimeoutError):
        return True
    if isinstance(exc, OSError) and getattr(exc, "errno", None) in RETRYABLE_ERRNOS:
        return True
    reason = getattr(exc, "reason", None)
    return isinstance(reason, OSError) and getattr(reason, "errno", None) in RETRYABLE_ERRNOS


def _open_with_retry(request: Request, timeout: int):
    last_exc = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            return urlopen(request, timeout=timeout)
        except (URLError, OSError, TimeoutError, ValueError) as exc:
            last_exc = exc
            if attempt >= MAX_RETRIES or not _is_retryable(exc):
                raise
            time.sleep(BACKOFF_SECONDS * (2 ** attempt))
    raise last_exc  # pragma: no cover


SEARCH_ENGINE_HOSTS = {
    "google.com", "www.google.com", "bing.com", "www.bing.com",
    "duckduckgo.com", "www.duckduckgo.com",
}

SOCIAL_HOSTS = {
    "facebook.com", "www.facebook.com", "m.facebook.com",
    "instagram.com", "www.instagram.com",
    "tiktok.com", "www.tiktok.com",
    "youtube.com", "www.youtube.com",
    "linkedin.com", "www.linkedin.com",
    "x.com", "www.x.com", "twitter.com", "www.twitter.com",
    "pinterest.com", "www.pinterest.com",
    "threads.net", "www.threads.net",
    "snapchat.com", "www.snapchat.com",
    "reddit.com", "www.reddit.com",
}


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def _normalize_result_url(href: str) -> str | None:
    href = unquote(href)
    if href.startswith("//"):
        href = "https:" + href
    parsed = urlparse(href)
    if parsed.scheme not in {"http", "https"}:
        return None

    host_lower = parsed.netloc.lower()
    if "duckduckgo.com" in host_lower:
        real = parse_qs(parsed.query).get("uddg", [None])[0]
        if real:
            href = real
            parsed = urlparse(href)
    elif "bing.com" in host_lower:
        real = parse_qs(parsed.query).get("u", [None])[0]
        if real:
            href = real
            parsed = urlparse(href)
    elif "google." in host_lower:
        real = parse_qs(parsed.query).get("q", [None])[0]
        if real and real.startswith(("http://", "https://")):
            href = real
            parsed = urlparse(href)
        elif parsed.path == "/goto":
            # Google now uses opaque /goto redirects for many organic results.
            # Resolve the public redirect only; never treat Google itself as the
            # business target. The destination is then stored as search provenance.
            try:
                request = Request(
                    href,
                    headers={"User-Agent": "Mozilla/5.0 (compatible; ORVIA-AGI/2.5)"}
                )
                with _open_with_retry(request, timeout=5) as response:
                    final_url = response.geturl()
                final = urlparse(final_url)
                if final.scheme in {"http", "https"} and final.netloc:
                    href = final_url
                    parsed = final
            except Exception:
                return None

    host = parsed.netloc.lower()
    clean_host = host.removeprefix("www.")
    blocked = {h.removeprefix("www.") for h in SEARCH_ENGINE_HOSTS}
    social = {h.removeprefix("www.") for h in SOCIAL_HOSTS}
    if not clean_host or clean_host in blocked or any(clean_host.endswith("." + b) for b in blocked):
        return None
    # Discovery is for business targets, not social profiles/search pages.
    if clean_host in social or any(clean_host.endswith("." + s) for s in social):
        return None
    path = (parsed.path or "/").lower()
    if any(token in path for token in (
        "/search", "/directory", "/directories", "/blog", "/article",
        "/articles", "/reports/", "/report/", "/news/", "/statistics",
        "/country-commercial-guides/", "/technologies/",
    )):
        return None

    return f"{parsed.scheme}://{parsed.netloc}{parsed.path or '/'}"


def _search(url: str) -> list[str]:
    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; ORVIA-AGI/2.5; +public-discovery)"}
    )
    with _open_with_retry(request, timeout=8) as response:
        html = response.read().decode("utf-8", errors="ignore")
    parser = _LinkParser()
    parser.feed(html)
    return parser.links


def _provider_urls(query: str) -> list[str]:
    q = quote_plus(query)
    return [
        f"https://html.duckduckgo.com/html/?q={q}",
        f"https://www.bing.com/search?q={q}&count=10",
        f"https://www.google.com/search?q={q}&num=10",
    ]


def _platform_for_url(url: str) -> str:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    if host.endswith("facebook.com"):
        return "facebook"
    if host.endswith("instagram.com"):
        return "instagram"
    if host.endswith("tiktok.com"):
        return "tiktok"
    if host.endswith("youtube.com"):
        return "youtube"
    if host.endswith("linkedin.com"):
        return "linkedin"
    if host.endswith(("x.com", "twitter.com")):
        return "x"
    if host.endswith("pinterest.com"):
        return "pinterest"
    if host.endswith("threads.net"):
        return "threads"
    if host.endswith("snapchat.com"):
        return "snapchat"
    if host.endswith("reddit.com"):
        return "reddit"
    return "web"


def discovery_catalog() -> list[dict[str, object]]:
    """Return the complete configured source catalog for monitoring."""
    return source_catalog()


def discovery_status() -> dict[str, object]:
    return {
        "status": "ready",
        "scope": "internet-wide public/authorized sources",
        "catalog_sources": len(SOURCES),
        "active_search_providers": ["Google Search", "Bing Search", "DuckDuckGo"],
        "social_domains_supported": sorted({x.removeprefix("www.") for x in SOCIAL_HOSTS}),
        "policy": "public_or_authorized_access_only",
        "next_expansion": "add official APIs/connectors without changing the discovery interface",
    }


_LAST_DISCOVERY_PROVENANCE: dict[str, dict[str, object]] = {}


def discovery_provenance(url: str) -> dict[str, object] | None:
    """Return provenance captured when a URL was discovered."""
    item = _LAST_DISCOVERY_PROVENANCE.get(url)
    return dict(item) if item else None


_LAST_DISCOVERY_STATUS: dict[str, object] = {
    "status": "never_run",
    "providers": {},
    "found": 0,
    "fallback_used": False,
}

def discovery_runtime_status() -> dict[str, object]:
    return {
        "status": _LAST_DISCOVERY_STATUS.get("status", "unknown"),
        "providers": dict(_LAST_DISCOVERY_STATUS.get("providers", {})),
        "found": int(_LAST_DISCOVERY_STATUS.get("found", 0)),
        "fallback_used": bool(_LAST_DISCOVERY_STATUS.get("fallback_used", False)),
    }

def discover_prospects(max_targets: int = 10, queries: list[str] | None = None) -> list[str]:
    """Discover public business websites and public social profiles across major platforms."""
    if max_targets <= 0:
        return []

    raw = os.getenv("HAMED_DISCOVERY_QUERIES", "")
    search_queries = (
        queries
        or [q.strip() for q in raw.split(",") if q.strip()]
        or DEFAULT_DISCOVERY_QUERIES
    )
    found: list[str] = []
    seen: set[str] = set()
    _LAST_DISCOVERY_PROVENANCE.clear()
    provider_status: dict[str, object] = {}

    # Prefer commercial-intent queries first while preserving caller-provided
    # queries. This improves the chance that the first cycle produces real
    # business targets rather than informational pages.
    priority_terms = ("online store", "ecommerce", "shop", "restaurant online ordering", "small business")
    search_queries = sorted(
        search_queries,
        key=lambda q: 0 if any(term in q.lower() for term in priority_terms) else 1,
    )

    for query in search_queries:
        if len(found) >= max_targets:
            break
        for provider_url in _provider_urls(query):
            provider_host = urlparse(provider_url).netloc.lower()
            try:
                links = _search(provider_url)
                provider_status[provider_host] = {"status": "ok", "results": len(links)}
            except Exception as exc:  # noqa: BLE001 - provider/network boundary
                provider_status[provider_host] = {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
                continue
            for href in links:
                target = _normalize_result_url(href)
                if target and target not in seen:
                    seen.add(target)
                    _LAST_DISCOVERY_PROVENANCE[target] = {
                        "source": "search",
                        "provider": provider_host,
                        "query": query,
                    }
                    found.append(target)
                    if len(found) >= max_targets:
                        break
            if len(found) >= max_targets:
                break

    fallback_used = False
    if not found:
        fallback_used = True
        for url in FALLBACK_BUSINESS_URLS:
            target = _normalize_result_url(url)
            if target and target not in seen:
                seen.add(target)
                _LAST_DISCOVERY_PROVENANCE[target] = {
                    "source": "fallback",
                    "provider": None,
                    "query": None,
                }
                found.append(target)
                if len(found) >= max_targets:
                    break

    _LAST_DISCOVERY_STATUS.update({
        "status": "ok" if found else "empty",
        "providers": provider_status,
        "found": len(found),
        "fallback_used": fallback_used,
    })
    return found
