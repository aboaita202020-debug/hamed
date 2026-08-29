"""Minimal local Hamed server entrypoint for Windows development."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Hamed AI Local Server", version="0.1.0")

@app.get("/")
def root():
    return {"name": "Hamed AI", "status": "running", "mode": "local"}

@app.get("/health")
def health():
    return JSONResponse({"status": "ok", "voice": "disabled", "paid_integrations": "disabled"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("local_server:app", host="127.0.0.1", port=8000, reload=False)
