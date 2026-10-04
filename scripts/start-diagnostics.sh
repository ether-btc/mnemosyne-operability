#!/bin/bash
# Diagnostics service wrapper
# Usage: ./start-diagnostics.sh [start|stop|status|restart]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="/tmp/diagnostics.pid"
LOG_FILE="/home/hermes-pi/.hermes/cache/scratch/diagnostics.log"

start() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "Already running (pid $(cat "$PID_FILE"))"
        return 1
    fi
    nohup python3 "$SCRIPT_DIR/diagnostics.py" >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "Started diagnostics (pid $!)"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        kill "$(cat "$PID_FILE")" 2>/dev/null
        rm -f "$PID_FILE"
        echo "Stopped diagnostics"
    else
        echo "Not running"
    fi
}

status() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "Running (pid $(cat "$PID_FILE"))"
        ps -p "$(cat "$PID_FILE")" -o pid,etime,cmd --no-headers
    else
        echo "Not running"
    fi
}

case "${1:-start}" in
    start)  start ;;
    stop)   stop ;;
    status) status ;;
    restart) stop; sleep 1; start ;;
    *)      echo "Usage: $0 {start|stop|status|restart}"; exit 1 ;;
esac
