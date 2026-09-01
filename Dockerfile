FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Telegram polling is the primary runtime. The FastAPI health endpoint is
# started in the same container by bot.py so /health remains available.
CMD ["python", "bot.py"]
