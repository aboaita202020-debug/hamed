"""
Hamed AI - Autonomous AI Business Operating System
====================================================
Core package. Only stdlib is imported here so that the Core
(orchestrator, agents, permissions, CRM) can start and be tested
without any third-party dependency installed.

Optional adapters (Telegram, FastAPI dashboard, OpenAI/Claude SDKs)
live in their own sub-packages and import their third-party
dependency lazily / defensively, so a missing package there never
breaks the Core.
"""

__version__ = "0.1.0"
