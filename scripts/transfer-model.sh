#!/bin/bash
# Binary-safe model transfer from a16 to Pi.
# Usage: transfer-model.sh <remote-path> <local-path>

set -uo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <remote-path> <local-path>"
    echo "Example: $0 C:\\Users\\kranl\\bekko\\bekko-decider\\output\\model ./evidence/model"
    exit 1
fi

REMOTE_PATH="$1"
LOCAL_PATH="$2"

echo "=== Transferring model from a16 ==="
echo "Remote: $REMOTE_PATH"
echo "Local: $LOCAL_PATH"
echo ""

# Create local directory
mkdir -p "$LOCAL_PATH"

# Transfer via tar over SSH (binary safe)
ssh a16 "tar czf - -C '$REMOTE_PATH' ." | tar xzf - -C "$LOCAL_PATH"

if [ $? -eq 0 ]; then
    echo ""
    echo "=== Transfer complete ==="
    echo "Files:"
    find "$LOCAL_PATH" -type f | head -10
    echo ""
    echo "Total size: $(du -sh "$LOCAL_PATH" | cut -f1)"
else
    echo ""
    echo "ERROR: Transfer failed"
    exit 1
fi
