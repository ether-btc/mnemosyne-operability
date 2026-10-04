#!/usr/bin/env python3
"""R0b local positive-control canary wrapper.

Opens state.db in read-only mode, runs a metadata-only query (IDs only,
no content), and emits only an allowlisted boolean/count receipt.

Isolation properties:
- Runs with python3 -I (isolated mode)
- Only imports stdlib modules (sqlite3, json, sys, hashlib, logging)
- Only opens state.db in read-only mode (mode=ro URI)
- No subprocess, no file writes, no network, no credential access
- Output is exactly one JSON record on stdout
"""
import hashlib
import json
import logging
import sqlite3
import sys

DB_PATH = "/home/hermes-pi/.hermes/state.db"
# Fixed query parameters for the positive control
# These would be set per-canary-run in a private manifest
EXPECTED_SESSION_ID = "20260908_215448_0ee010"
EXPECTED_MESSAGE_ID = 208097
QUERY = "SELECT id, session_id FROM messages WHERE session_id = ? AND id = ? LIMIT 1"


def main():
    # Suppress all logging before any imports that might log
    logging.disable(logging.CRITICAL)

    # Open state.db in read-only mode
    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        conn.execute("PRAGMA query_only = ON")
    except Exception as exc:
        print(f"ERROR: cannot open state.db read-only: {type(exc).__name__}", file=sys.stderr)
        sys.exit(1)

    try:
        # Run the metadata-only query
        row = conn.execute(QUERY, (EXPECTED_SESSION_ID, EXPECTED_MESSAGE_ID)).fetchone()

        # Check if the expected IDs match
        if row is None:
            positive_control = False
            match_count = 0
        else:
            msg_id, session_id = row
            positive_control = (msg_id == EXPECTED_MESSAGE_ID and session_id == EXPECTED_SESSION_ID)
            match_count = 1 if positive_control else 0

        # Emit only the allowlisted receipt
        receipt = {
            "schema_version": 1,
            "probe_id": hashlib.sha256(f"{EXPECTED_SESSION_ID}:{EXPECTED_MESSAGE_ID}".encode()).hexdigest()[:16],
            "positive_control": positive_control,
            "match_count": match_count,
        }
        print(json.dumps(receipt))

    except Exception as exc:
        print(f"ERROR: query failed: {type(exc).__name__}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
