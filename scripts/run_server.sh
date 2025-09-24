#!/usr/bin/env bash
set -eu

# Background uvicorn manager for development
# Usage: scripts/run_server.sh {start|stop|restart|status|logs}

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT_DIR/.venv"
PID_FILE="/tmp/uvicorn_bg.pid"
LOG_FILE="/tmp/uvicorn_bg.out"
APP_MODULE="app.main:app"
HOST="127.0.0.1"
PORT="8000"

activate_venv() {
  if [ -f "$VENV/bin/activate" ]; then
    # shellcheck source=/dev/null
    . "$VENV/bin/activate"
  else
    echo "Warning: virtualenv not found at $VENV — continuing with system python"
  fi
}

start() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Server already running (pid=$(cat "$PID_FILE"))"
    return 0
  fi

  activate_venv
  nohup python -m uvicorn $APP_MODULE --host $HOST --port $PORT >"$LOG_FILE" 2>&1 &
  echo $! >"$PID_FILE"
  echo "Started uvicorn (pid=$(cat "$PID_FILE")), logs: $LOG_FILE"
}

stop() {
  if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid"
      echo "Sent SIGTERM to $pid"
    else
      echo "Process $pid not running"
    fi
    rm -f "$PID_FILE"
  else
    echo "No pid file found at $PID_FILE"
  fi
}

status() {
  if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Running (pid=$(cat "$PID_FILE"))"
  else
    echo "Not running"
  fi
}

logs() {
  tail -n 200 -F "$LOG_FILE"
}

case "${1-}" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop || true
    sleep 0.3
    start
    ;;
  status)
    status
    ;;
  logs)
    logs
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status|logs}"
    exit 2
    ;;
esac
