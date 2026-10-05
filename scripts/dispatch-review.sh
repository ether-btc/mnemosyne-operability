#!/bin/bash
# Dispatch all 3 review bots in parallel.
# Usage: dispatch-review.sh <prompt-file> <output-dir>

set -uo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <prompt-file> <output-dir>"
    exit 1
fi

PROMPT_FILE="$1"
OUTPUT_DIR="$2"

mkdir -p "$OUTPUT_DIR"

echo "=== Dispatching 3 review bots in parallel ==="
echo ""

# Dispatch all 3 bots in parallel
hermes -p vibe-coding-expert -z "$(cat "$PROMPT_FILE")" > "$OUTPUT_DIR/vibe.txt" 2>&1 &
PID_VIBE=$!

hermes -p technical-cofounder -z "$(cat "$PROMPT_FILE")" > "$OUTPUT_DIR/cofounder.txt" 2>&1 &
PID_COFOUNDER=$!

hermes -p reviewer -z "$(cat "$PROMPT_FILE")" > "$OUTPUT_DIR/reviewer.txt" 2>&1 &
PID_REVIEWER=$!

echo "Dispatched: vibe (pid $PID_VIBE), cofounder (pid $PID_COFOUNDER), reviewer (pid $PID_REVIEWER)"
echo "Waiting for completion..."
echo ""

# Wait for all to complete
wait $PID_VIBE
VIBE_RC=$?
wait $PID_COFOUNDER
COFOUNDER_RC=$?
wait $PID_REVIEWER
REVIEWER_RC=$?

echo ""
echo "=== Results ==="
echo "Vibe: exit $VIBE_RC"
echo "Cofounder: exit $COFOUNDER_RC"
echo "Reviewer: exit $REVIEWER_RC"
echo ""
echo "Outputs saved to: $OUTPUT_DIR"
echo "  - vibe.txt"
echo "  - cofounder.txt"
echo "  - reviewer.txt"
