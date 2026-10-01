from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class WebSource:
    name: str
    category: str
    access: str
    discovery: str
    notes: str


SOURCES: tuple[WebSource, ...] = (
    WebSource("Google Search", "search", "api_or_authorized", "search queries", "Use an approved API; no bypassing access controls."),
    WebSource("Bing Search", "search", "api_or_authorized", "search queries", "Use an approved API."),
    WebSource("DuckDuckGo", "search", "public_or_authorized", "search queries", "Respect rate limits and terms."),
    WebSource("Google News", "news", "api_or_authorized", "news discovery", "Public/authorized feeds only."),
    WebSource("Reddit", "community", "api_or_authorized", "public discussions", "Respect API rules and privacy."),
    WebSource("YouTube", "video", "api_or_authorized", "channels/videos/signals", "Use public data or authorized analytics."),
    WebSource("TikTok", "social", "api_or_authorized", "public signals", "Use permitted APIs and public information."),
    WebSource("Facebook", "social", "api_or_authorized", "public pages/signals", "Do not access private profiles or restricted data."),
    WebSource("Instagram", "social", "api_or_authorized", "public/business signals", "Use permitted APIs and public information."),
    WebSource("X", "social", "api_or_authorized", "public posts/signals", "Use permitted APIs and public information."),
    WebSource("LinkedIn", "professional", "api_or_authorized", "public/company signals", "No unauthorized scraping or private-data collection."),
    WebSource("Public business directories", "business", "public_or_authorized", "company discovery", "Only public business information."),
    WebSource("Public company websites", "web", "public_or_authorized", "site analysis", "Honor robots, terms, rate limits, and access controls."),
    WebSource("E-commerce storefronts", "commerce", "public_or_authorized", "store discovery", "Analyze public storefront information."),
    WebSource("Public marketplaces", "commerce", "api_or_authorized", "product/merchant discovery", "Prefer official APIs or permitted feeds."),
    WebSource("Public forums", "community", "public_or_authorized", "need/signal discovery", "Avoid private communities and sensitive profiling."),
    WebSource("Public blogs", "content", "public_or_authorized", "topic discovery", "Use public pages and feeds."),
    WebSource("RSS/Atom feeds", "feeds", "public_or_authorized", "continuous monitoring", "Respect publisher terms and feed limits."),
    WebSource("GitHub public repositories", "developer", "api_or_authorized", "software/project discovery", "Use GitHub APIs and repository terms."),
    WebSource("Public datasets", "data", "public_or_authorized", "structured discovery", "Track license and provenance."),
    WebSource("Open government data", "data", "public_or_authorized", "market/public signals", "Use datasets according to their licenses."),
    WebSource("Public procurement portals", "business", "public_or_authorized", "contract/opportunity discovery", "Respect portal rules."),
    WebSource("Public job boards", "business", "public_or_authorized", "business hiring signals", "Collect business-level signals; avoid sensitive profiling."),
    WebSource("Public app stores", "software", "public_or_authorized", "product discovery", "Use public listings and permitted APIs."),
    WebSource("Public review platforms", "commerce", "public_or_authorized", "customer pain signals", "Aggregate themes; do not expose personal data."),
    WebSource("Public trend platforms", "trends", "api_or_authorized", "trend discovery", "Use official or permitted interfaces."),
    WebSource("Public event calendars", "events", "public_or_authorized", "event/business discovery", "Use public event information."),
    WebSource("Public podcast directories", "media", "public_or_authorized", "content/business discovery", "Use feeds and public metadata."),
    WebSource("Public academic/research indexes", "research", "api_or_authorized", "research discovery", "Respect licenses and access restrictions."),
    WebSource("Public domain registries", "web", "public_or_authorized", "domain/business discovery", "Use lawful public registry data."),
)


def catalog() -> list[dict[str, Any]]:
    return [asdict(source) for source in SOURCES]


def status() -> dict[str, Any]:
    categories = sorted({source.category for source in SOURCES})
    return {
        "status": "ready",
        "scope": "internet-wide public/authorized sources",
        "source_count": len(SOURCES),
        "categories": categories,
        "policy": "public_or_authorized_access_only",
        "connector_model": "one adapter per source; unsupported sources remain discoverable in the catalog until configured",
    }
