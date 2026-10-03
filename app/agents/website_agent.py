"""Draft website packages for sellers without websites."""
from dataclasses import dataclass

@dataclass(frozen=True)
class WebsiteBrief:
    business_name: str
    category: str
    description: str
    contact: str

@dataclass(frozen=True)
class WebsiteDraft:
    title: str
    pages: tuple[str, ...]
    hero_copy: str
    contact: str


def create_draft(brief: WebsiteBrief) -> WebsiteDraft:
    if not brief.business_name.strip() or not brief.category.strip():
        raise ValueError("Business name and category are required")
    return WebsiteDraft(
        title=brief.business_name,
        pages=("Home", "Products/Services", "About", "Contact"),
        hero_copy=f"{brief.business_name} — {brief.description}",
        contact=brief.contact,
    )
