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

# Persistent SQLite data directory. Render Free uses ephemeral filesystem storage.
RUN mkdir -p /app/data

# Render provides PORT at runtime. Keep 8000 as the local/default fallback.
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os,urllib.request; p=os.getenv('PORT','8000'); urllib.request.urlopen(f'http://127.0.0.1:{p}/health', timeout=3)" || exit 1

# Render sets PORT automatically; shell expansion is required.
CMD ["sh", "-c", "uvicorn scripts.run_server:app --host 0.0.0.0 --port ${PORT:-8000}"]
