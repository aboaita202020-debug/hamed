# PythonAnywhere deployment

ORVIA AGI is a FastAPI/ASGI application. PythonAnywhere's current ASGI deployment is experimental; use its `pa` ASGI website tooling rather than the traditional WSGI web-app configuration.

## 1. Clone and install

    git clone https://github.com/aboaita202020-debug/hamed-agi.git ~/hamed-agi
    cd ~/hamed-agi
    mkvirtualenv orvia_venv --python=python3.11
    pip install -r requirements.txt

Run the verification before creating the website:

    python -m pytest -q
    python -c "from app.main import app; print(app.title, app.version)"

## 2. ASGI/Uvicorn command

The ASGI object is `app.main:app`. PythonAnywhere's ASGI system provides `DOMAIN_SOCKET`, so Uvicorn must bind to that Unix socket:

    /home/aboaita2011/.virtualenvs/orvia_venv/bin/uvicorn --app-dir /home/aboaita2011/hamed-agi --uds ${DOMAIN_SOCKET} app.main:app

Create the ASGI site with:

    pip install --upgrade pythonanywhere
    pa website create --domain aboaita2011.pythonanywhere.com --command '/home/aboaita2011/.virtualenvs/orvia_venv/bin/uvicorn --app-dir /home/aboaita2011/hamed-agi --uds ${DOMAIN_SOCKET} app.main:app'

Replace `aboaita2011` with the actual PythonAnywhere username.

## 3. Reload after updates

    cd ~/hamed-agi
    git pull
    source ~/.virtualenvs/orvia_venv/bin/activate
    pip install -r requirements.txt
    python -m pytest -q
    pa website reload --domain aboaita2011.pythonanywhere.com

## 4. Cloud verification

After the site is live, verify:

    curl -fsS https://aboaita2011.pythonanywhere.com/health
    curl -fsS https://aboaita2011.pythonanywhere.com/readiness
    curl -fsS https://aboaita2011.pythonanywhere.com/status
    curl -fsS -o /dev/null -w "%{http_code}\n" https://aboaita2011.pythonanywhere.com/dashboard

Expected: HTTP 200 for all four endpoints.

Keep API keys and other secrets in the PythonAnywhere environment; never commit them to Git.

`pythonanywhere_wsgi.py` is retained only for legacy WSGI compatibility. It is not the ASGI deployment entry point.


## 5. Autonomous commercial agent

The repository now includes a safe commercial operating loop:
- discover opportunities
- research configured public prospects
- qualify leads into CRM
- draft personalized offers
- record memory
- generate a cycle report

Configure public prospect URLs in the PythonAnywhere environment (comma-separated):

    ORVIA_AUTONOMOUS_ENABLED=true
    ORVIA_PROSPECT_URLS=https://example.com,https://example.org

Run one cycle manually:

    cd ~/hamed-agi
    /home/aboaita2011/.virtualenvs/orvia_venv/bin/python scripts/run_autonomous.py

The API also exposes:

    GET  /api/v1/autonomous/status
    POST /api/v1/autonomous/run

Use a PythonAnywhere Scheduled Task to run scripts/run_autonomous.py periodically. The loop does not purchase, pay, sign contracts, or perform irreversible financial/legal actions.
