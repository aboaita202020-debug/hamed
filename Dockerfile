# Hamed AI — Production Docker image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HAMED_ENV=production

WORKDIR /app

# System deps kept minimal on purpose — Core itself needs none.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Persistent SQLite data directory. Configure a Railway Volume separately.
# IMPORTANT: no native Docker VOLUME directive — Railway manages volumes.
RUN mkdir -p /app/data

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" || exit 1

# Runs the FastAPI dashboard/health/webhook server.
# Railway may override this with its configured start command.
CMD ["uvicorn", "scripts.run_server:app", "--host", "0.0.0.0", "--port", "8000"]
