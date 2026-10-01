# ORVIA AGI

ORVIA is a FastAPI/ASGI commercial operating system.

Runtime includes Core, Orchestrator, 200 specialist Agents, CRM, Opportunity Engine, Revenue Engine, AGI Engine, Dashboard, Health, Readiness and Status APIs.

## Internet-wide opportunity discovery

The discovery layer is designed as a connector-based system for public or authorized online sources. The source registry currently catalogs 30 source types/categories, including search engines, social platforms, public business sites, e-commerce, marketplaces, public datasets, feeds, developer platforms, public procurement and other public web signals.

The active discovery engine currently uses Google Search, Bing Search and DuckDuckGo as search providers and can discover public business websites and public social profiles. New official APIs/connectors can be added without changing the discovery interface.

Source catalog and runtime status are available from `app.web_source_registry` and `app.prospect_discovery`.

The system is intentionally limited to public or authorized access and should not bypass authentication, access controls, robots restrictions, rate limits, platform terms, or privacy protections.

## Run locally

    python -m pip install -r requirements.txt
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

## Tests

    python -m pytest -q

## PythonAnywhere

See PYTHONANYWHERE.md. The ASGI application object is app.main:app; use Uvicorn/ASGI configuration and keep secrets in the PythonAnywhere environment, never in Git.
