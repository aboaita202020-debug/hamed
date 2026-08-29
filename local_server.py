"""Backward-compatible local entrypoint.

Runs the full Hamed FastAPI application instead of a health-only stub.
"""
from app.main import app

if __name__ == "__main__":
    import os
    import uvicorn

    uvicorn.run(
        "local_server:app",
        host=os.getenv("HAMED_HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", os.getenv("HAMED_PORT", "8000"))),
        reload=False,
    )
