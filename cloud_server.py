"""Cloud entrypoint for Hamed AGI.

Expose the full application so cloud deployments do not accidentally run a
minimal health-only shell. Secrets remain environment-only.
"""
from app.main import app

__all__ = ["app"]

if __name__ == "__main__":
    import os
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("HAMED_HOST", "0.0.0.0"),
        port=int(os.getenv("HAMED_PORT", "8000")),
    )
