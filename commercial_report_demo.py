"""Commercial activation demo: real LLM + real web search + report generation.

Tests the three commercial functions:
1. Real LLM chat (Gemini/Groq)
2. Real web search (DuckDuckGo)
3. Commercial report generation using ResearchAgent + OfferCompilerAgent
"""
from __future__ import annotations

import sys
import time

from app.agents.provider import MultiBrainProvider
from app.agents.research_agent import ResearchAgent
from app.tools.web_search_duckduckgo import WebSearchToolWithDuckDuckGo


def main() -> int:
    print("=== ORVIA HAMED COMMERCIAL ACTIVATION DEMO ===")
    print()

    # 1. LLM connectivity
    print("[1] LLM connectivity")
    try:
        provider = MultiBrainProvider()
        print("  Available brains:", list(provider.available_brains()))
        t0 = time.time()
        reply = provider.generate_response(
            [{"role": "user", "content": "Reply with exactly: OK"}],
            system="Reply with only the word OK.",
        )
        print(f"  Chat OK in {time.time()-t0:.2f}s -> {reply!r}")
    except Exception as e:
        print("  FAILED:", e)
        return 1

    # 2. Web search
    print()
    print("[2] Web search (DuckDuckGo)")
    try:
        tool = WebSearchToolWithDuckDuckGo()
        t0 = time.time()
        res = tool.run("top 5 e-commerce companies in Egypt 2024", max_results=5)
        print(f"  Search OK in {time.time()-t0:.2f}s -> success={res.success}")
        if res.success:
            for i, item in enumerate(res.data[:3], 1):
                print(f"   {i}. {item['title']} | {item['url']}")
        else:
            print("  Error:", res.error)
    except Exception as e:
        print("  FAILED:", e)

    # 3. Research agent
    print()
    print("[3] Research agent")
    try:
        ra = ResearchAgent(provider)
        t0 = time.time()
        report = ra.research("What are the main e-commerce trends in Egypt and the Gulf in 2024?")
        print(f"  Research OK in {time.time()-t0:.2f}s")
        print("  Findings (first 400 chars):")
        print("  ", report.findings[:400].replace("\n", " "))
    except Exception as e:
        print("  FAILED:", e)

    # 4. Commercial report synthesis
    print()
    print("[4] Commercial report synthesis")
    try:
        query = "e-commerce market size Egypt 2024"
        search_res = tool.run(query, max_results=5)
        findings = ""
        if search_res.success:
            findings = "\n".join([f"{i['title']}: {i['snippet']}" for i in search_res.data])
        else:
            findings = "No web results."
        llm_summary = provider.generate_response(
            [{"role": "user", "content": f"Summarize e-commerce market size in Egypt 2024 in 3 bullet points. Use this web evidence:\n{findings}"}],
            system="You are a commercial analyst. Be concise and factual.",
        )
        print("  Report:")
        print(llm_summary)
    except Exception as e:
        print("  FAILED:", e)

    print()
    print("=== DEMO COMPLETE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
