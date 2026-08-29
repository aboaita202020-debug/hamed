"""Cloud entrypoint for Hamed AI.

Binds publicly so Oracle/Koyeb-style hosts can route HTTP traffic to Hamed.
Secrets are read from environment variables only.
"""
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Hamed AI", version="0.1.0")

@app.get("/")
def root():
    return {"name": "Hamed AI", "status": "running", "mode": "cloud"}

@app.get("/health")
def health():
    return JSONResponse({"status": "ok", "voice": "configured" if os.getenv("OPENAI_API_KEY") else "disabled", "paid_integrations": "configured" if os.getenv("TWILIO_ACCOUNT_SID") else "disabled"})

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HAMED_HOST", "0.0.0.0")
    port = int(os.getenv("HAMED_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
