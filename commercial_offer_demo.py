"""Commercial offer generation demo using OfferCompilerAgent + web evidence.

Demonstrates B2B offer creation with real LLM and optional web search.
"""
from __future__ import annotations

import sys
from app.agents.provider import MultiBrainProvider
from app.tools.web_search_brave import WebSearchToolWithBrave
from app.tools.web_search_duckduckgo import WebSearchToolWithDuckDuckGo


def generate_offer(provider, search_tool, company: str, product: str) -> str:
    # 1. Gather web evidence if available
    evidence = ""
    try:
        res = search_tool.run(f"{company} {product} price Egypt", max_results=5)
        if res.success:
            evidence = "\n".join([f"- {i['title']}: {i['snippet']}" for i in res.data])
        else:
            evidence = "No web evidence available."
    except Exception:
        evidence = "No web evidence available."

    # 2. Build prompt for offer
    prompt = f"""
You are a commercial offer compiler for Egypt/Gulf market.
Company: {company}
Product/Service: {product}

Web evidence:
{evidence}

Create a concise B2B commercial proposal in Arabic and English:
- Executive summary
- Value proposition
- Pricing estimate range
- Next steps

Be factual, do not invent prices if unknown.
"""
    reply = provider.generate_response(
        [{"role": "user", "content": prompt}],
        system="You are a commercial analyst. Be concise and factual.",
    )
    return reply


def main() -> int:
    print("=== COMMERCIAL OFFER DEMO ===")
    provider = MultiBrainProvider()
    print("Brains:", list(provider.available_brains()))

    # Try Brave first, fallback to DuckDuckGo
    brave_tool = WebSearchToolWithBrave()
    duck_tool = WebSearchToolWithDuckDuckGo()
    search_tool = brave_tool if brave_tool.provider.api_key else duck_tool
    print("Search provider:", "Brave" if brave_tool.provider.api_key else "DuckDuckGo (may be blocked)")

    company = "Salla"
    product = "e-commerce platform"
    offer = generate_offer(provider, search_tool, company, product)
    print("\n--- OFFER ---\n")
    print(offer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
