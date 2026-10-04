#!/usr/bin/env python3
"""Automated diagnostics module for RPi5.

Monitors:
1. Training jobs (process alive, log growth, exit codes)
2. Model services (port health: 8099, 8086, etc.)
3. System health (disk, memory, CPU)
4. Log scanning (error patterns in training/wandb/hermes logs)

Alerts sent via hermes bot messaging. State persisted in SQLite.
"""
import json
import logging
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import psutil

# --- Configuration ---
DB_PATH = Path("/home/hermes-pi/.hermes/cache/scratch/diagnostics.db")
LOG_PATH = Path("/home/hermes-pi/.hermes/cache/scratch/diagnostics.log")
ALERT_COOLDOWN = 300  # seconds between duplicate alerts
CHECK_INTERVAL = 60  # seconds

# Model ports to monitor
MODEL_PORTS = {
    8099: "qwen2.5-1.5b",
    8086: "decider-0.8b",
    8080: "qwen2.5-0.5b",
}

# Training job patterns (process name -> description)
TRAINING_PATTERNS = [
    (re.compile(r"bekko_system_one\.training"), "Bekko training"),
    (re.compile(r"llama-server"), "llama-server"),
]

# Log paths to scan
LOG_PATHS = [
    Path("/home/hermes-pi/.hermes/cache/scratch"),
    Path("/home/hermes-pi/projects/mnemosyne-operability"),
]

# Error patterns to scan for
ERROR_PATTERNS = [
    re.compile(r"Traceback \(most recent call last\)"),
    re.compile(r"FileExistsError"),
    re.compile(r"CUDA out of memory"),
    re.compile(r"OutOfMemoryError"),
    re.compile(r"Connection refused"),
    re.compile(r"ERROR"),
]

# System thresholds
DISK_THRESHOLD = 90  # percent
MEMORY_THRESHOLD = 85  # percent
CPU_THRESHOLD = 90  # percent


def init_db():
    """Initialize SQLite database for alert persistence."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL,
            details TEXT,
            acknowledged INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS training_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER,
            name TEXT,
            start_time TEXT,
            last_log_size INTEGER,
            last_check TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()


def send_alert(category, severity, message, details=None):
    """Send alert via hermes bot messaging and persist to DB."""
    # Check cooldown
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT timestamp FROM alerts WHERE category = ? AND message = ? ORDER BY timestamp DESC LIMIT 1",
        (category, message),
    ).fetchone()
    if row:
        last = datetime.fromisoformat(row[0])
        if datetime.now() - last < timedelta(seconds=ALERT_COOLDOWN):
            conn.close()
            return  # Skip duplicate

    # Persist
    conn.execute(
        "INSERT INTO alerts (timestamp, category, severity, message, details) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), category, severity, message, details),
    )
    conn.commit()
    conn.close()

    # Send via hermes
    alert_text = f"[{severity}] {category}: {message}"
    if details:
        alert_text += f"\n{details}"
    try:
        subprocess.run(
            ["hermes", "-p", "sentry", "-z", alert_text],
            timeout=10,
            capture_output=True,
        )
    except Exception as e:
        logging.warning(f"Failed to send alert: {e}")

    logging.warning(alert_text)


def check_training_jobs():
    """Monitor training processes for silent deaths."""
    conn = sqlite3.connect(DB_PATH)
    tracked = conn.execute("SELECT pid, name, last_log_size, status FROM training_jobs").fetchall()

    for pid, name, last_size, status in tracked:
        if status == "completed":
            continue
        if not psutil.pid_exists(pid):
            send_alert("training", "CRITICAL", f"Training process died: {name} (pid {pid})")
            conn.execute("UPDATE training_jobs SET status = ? WHERE pid = ?", ("dead", pid))
        else:
            # Check log growth
            log_files = list(Path("/home/hermes-pi/.hermes/cache/scratch").glob("run-*.log"))
            for log_file in log_files:
                size = log_file.stat().st_size
                if size == last_size:
                    send_alert("training", "WARNING", f"Training log not growing: {log_file.name}")
                conn.execute(
                    "UPDATE training_jobs SET last_log_size = ?, last_check = ? WHERE pid = ?",
                    (size, datetime.now().isoformat(), pid),
                )

    conn.commit()
    conn.close()


def check_model_services():
    """Health-check local model ports."""
    for port, name in MODEL_PORTS.items():
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            if result != 0:
                send_alert("model_service", "WARNING", f"Model service down: {name} on port {port}")
        except Exception as e:
            send_alert("model_service", "ERROR", f"Health check failed for {name}: {e}")


def check_system_health():
    """Check disk, memory, CPU thresholds."""
    # Disk
    disk = psutil.disk_usage("/")
    if disk.percent > DISK_THRESHOLD:
        send_alert("system", "CRITICAL", f"Disk usage {disk.percent}% (threshold {DISK_THRESHOLD}%)")

    # Memory
    mem = psutil.virtual_memory()
    if mem.percent > MEMORY_THRESHOLD:
        send_alert("system", "WARNING", f"Memory usage {mem.percent}% (threshold {MEMORY_THRESHOLD}%)")

    # CPU (1-min average)
    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_THRESHOLD:
        send_alert("system", "WARNING", f"CPU usage {cpu}% (threshold {CPU_THRESHOLD}%)")


def scan_logs():
    """Scan recent log files for error patterns."""
    cutoff = time.time() - 300  # Last 5 minutes
    for base in LOG_PATHS:
        if not base.exists():
            continue
        for log_file in base.glob("*.log"):
            if log_file.stat().st_mtime < cutoff:
                continue
            try:
                content = log_file.read_text(errors="ignore")
                for pattern in ERROR_PATTERNS:
                    if pattern.search(content):
                        send_alert("log_scan", "ERROR", f"Error pattern in {log_file.name}: {pattern.pattern}")
                        break
            except Exception:
                pass


def main():
    """Main monitoring loop."""
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    init_db()
    logging.info("Diagnostics module started")

    while True:
        try:
            check_training_jobs()
            check_model_services()
            check_system_health()
            scan_logs()
        except Exception as e:
            logging.error(f"Monitor loop error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
