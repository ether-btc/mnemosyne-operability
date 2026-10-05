#!/bin/bash
# Automated retry with exponential backoff.
# Usage: retry.sh <max-retries> <command...>

set -uo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <max-retries> <command...>"
    echo "Example: $0 3 curl -s http://example.com"
    exit 1
fi

MAX_RETRIES="$1"
shift

RETRY=0
DELAY=1

while [ $RETRY -lt $MAX_RETRIES ]; do
    echo "=== Attempt $((RETRY + 1))/$MAX_RETRIES ==="
    
    if "$@"; then
        echo ""
        echo "=== Success on attempt $((RETRY + 1)) ==="
        exit 0
    fi
    
    RETRY=$((RETRY + 1))
    
    if [ $RETRY -lt $MAX_RETRIES ]; then
        echo "Retrying in ${DELAY}s..."
        sleep $DELAY
        DELAY=$((DELAY * 2))
    fi
done

echo ""
echo "=== Failed after $MAX_RETRIES attempts ==="
exit 1
