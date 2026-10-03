#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="${VIRTUAL_ENV:-$HOME/.virtualenvs/hamed_venv}"
PYTHON="$VENV/bin/python"
WORKER="$ROOT/scripts/autonomous_worker.py"
LOG="$ROOT/data/autonomous_supervisor.log"
PIDFILE="$ROOT/data/autonomous_worker.pid"
CHECK_INTERVAL="${HAMED_SUPERVISOR_INTERVAL:-30}"

mkdir -p "$ROOT/data"
cd "$ROOT"

if [ ! -x "$PYTHON" ]; then
  echo "$(date -Is) ERROR: Python venv not found: $PYTHON" >> "$LOG"
  exit 1
fi

echo "$(date -Is) supervisor started" >> "$LOG"

while true; do
  PID=""
  if [ -f "$PIDFILE" ]; then
    PID="$(cat "$PIDFILE" 2>/dev/null || true)"
  fi

  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    sleep "$CHECK_INTERVAL"
    continue
  fi

  # Recover if the pidfile is stale or the worker crashed.
  PID="$(pgrep -f "python.*scripts/autonomous_worker.py" | head -n 1 || true)"
  if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    echo "$PID" > "$PIDFILE"
    sleep "$CHECK_INTERVAL"
    continue
  fi

  echo "$(date -Is) worker missing; starting it" >> "$LOG"
  nohup "$PYTHON" -u "$WORKER" >> "$ROOT/data/autonomous_worker.log" 2>&1 &
  NEW_PID=$!
  echo "$NEW_PID" > "$PIDFILE"
  echo "$(date -Is) worker started pid=$NEW_PID" >> "$LOG"
  sleep 5
done
