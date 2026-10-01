from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.error import URLError
import time
from urllib.parse import parse_qs, quote_plus, unquote, urljoin, urlparse
from urllib.request import Request, urlopen


@dataclass
class Evidence:
    url: str
    collected_at: str
    status_code: int | None
    title: str = ""
    notes: str = ""
    evidence_type: str = "direct_page"


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


class PublicResearch:
    SEARCH_PROVIDERS = (
        "https://html.duckduckgo.com/html/?q={q}",
        "https://www.bing.com/search?q={q}&count=10",
        "https://www.google.com/search?q={q}&num=10",
    )

    RETRYABLE_ERRNOS = {98, 99, 101, 104, 110, 111, 113}
    MAX_RETRIES = 2
    BACKOFF_SECONDS = 0.35

    @classmethod
    def _is_retryable(cls, exc: BaseException) -> bool:
        if isinstance(exc, TimeoutError):
            return True
        if isinstance(exc, OSError) and getattr(exc, "errno", None) in cls.RETRYABLE_ERRNOS:
            return True
        reason = getattr(exc, "reason", None)
        if isinstance(reason, OSError) and getattr(reason, "errno", None) in cls.RETRYABLE_ERRNOS:
            return True
        return False

    @classmethod
    def _open_with_retry(cls, request: Request, timeout: int):
        last_exc: BaseException | None = None
        for attempt in range(cls.MAX_RETRIES + 1):
            try:
                return urlopen(request, timeout=timeout)
            except (URLError, OSError, TimeoutError, ValueError) as exc:
                last_exc = exc
                if attempt >= cls.MAX_RETRIES or not cls._is_retryable(exc):
                    raise
                time.sleep(cls.BACKOFF_SECONDS * (2 ** attempt))
        raise last_exc  # pragma: no cover

    @staticmethod
    def _network_error_code(exc: BaseException) -> str:
        """Normalize common outbound-network failures for dashboards and reports."""
        errno = getattr(exc, "errno", None)
        reason = getattr(exc, "reason", None)
        reason_errno = getattr(reason, "errno", None)
        code = reason_errno if reason_errno is not None else errno
        if code == 111:
            return "connection_refused"
        if code == 99:
            return "cannot_assign_address"
        if code in {110} or isinstance(exc, TimeoutError):
            return "timeout"
        if code in {101, 113}:
            return "network_unreachable"
        if code in {98, 104}:
            return "socket_error"
        if isinstance(exc, ValueError):
            return "invalid_url"
        if isinstance(exc, URLError):
            return "url_error"
        return type(exc).__name__.lower()

    @staticmethod
    def _normalize_result_url(href: str) -> str | None:
        href = unquote(href)
        parsed = urlparse(href)
        if parsed.scheme not in {"http", "https"}:
            return None
        host = parsed.netloc.lower()
        if "duckduckgo.com" in host:
            href = parse_qs(parsed.query).get("uddg", [href])[0]
        elif "bing.com" in host:
            href = parse_qs(parsed.query).get("u", [href])[0]
        elif "google.com" in host:
            query_params = parse_qs(parsed.query)
            href = query_params.get("q", query_params.get("url", [href]))[0]
        parsed = urlparse(href)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return None
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path or '/'}"

    def _search_provider(self, provider_url: str) -> list[str]:
        req = Request(
            provider_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ORVIA-Research-Gateway/1.0)"}
        )
        with self._open_with_retry(req, timeout=8) as response:
            html = response.read().decode("utf-8", errors="ignore")
        parser = _LinkParser()
        parser.feed(html)
        return [urljoin(provider_url, href) for href in parser.links]

    def _gateway_research(self, url: str) -> Evidence | None:
        host = urlparse(url).netloc.lower().removeprefix("www.")
        if not host:
            return None

        corroborated: list[str] = []
        for template in self.SEARCH_PROVIDERS:
            query = quote_plus(f"site:{host}")
            provider_url = template.format(q=query)
            provider_host = urlparse(provider_url).netloc.lower()
            try:
                links = self._search_provider(provider_url)
            except (URLError, OSError, TimeoutError):
                continue

            matched = False
            for href in links:
                target = self._normalize_result_url(href)
                if not target:
                    continue
                target_host = urlparse(target).netloc.lower().removeprefix("www.")
                if target_host == host or target_host.endswith("." + host):
                    matched = True
                    break
            if matched:
                corroborated.append(provider_host)

        if len(corroborated) < 1:
            return None

        now = datetime.now(timezone.utc).isoformat()
        return Evidence(
            url=url,
            collected_at=now,
            status_code=200,
            title=host,
            notes=(
                "research_gateway: direct_page_fetch_unavailable; "
                f"search_corroboration={','.join(corroborated)}; "
                "identity_only=true; page_content_not_verified"
            ),
            evidence_type="search_corroborated",
        )

    def fetch(self, url: str, timeout: int = 8) -> Evidence:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return Evidence(
                url, datetime.now(timezone.utc).isoformat(), None,
                notes="invalid_public_url", evidence_type="invalid"
            )
        try:
            req = Request(url, headers={"User-Agent": "ORVIA-AGI/2.5"})
            with self._open_with_retry(req, timeout=timeout) as response:
                body = response.read(20000).decode("utf-8", errors="ignore")
                lower = body.lower()
                title = ""
                start = lower.find("<title>")
                end = lower.find("</title>", start + 7) if start >= 0 else -1
                if start >= 0 and end > start:
                    title = body[start + 7:end].strip()[:300]
                return Evidence(
                    url, datetime.now(timezone.utc).isoformat(), response.status,
                    title, "public evidence collected", "direct_page"
                )
        except (URLError, OSError, TimeoutError, ValueError) as exc:
            gateway = self._gateway_research(url)
            if gateway is not None:
                return gateway
            error_code = self._network_error_code(exc)
            return Evidence(
                url, datetime.now(timezone.utc).isoformat(), None,
                notes=f"network_error={error_code}; {type(exc).__name__}: {exc}",
                evidence_type="unverified"
            )


research = PublicResearch()
