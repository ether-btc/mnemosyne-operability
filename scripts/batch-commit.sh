#!/bin/bash
# Batch commit all changes with one descriptive message.
# Usage: batch-commit.sh <commit-message> [files...]

set -uo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <commit-message> [files...]"
    echo "Example: $0 \"Add model training and deployment\" scripts/ evidence/"
    exit 1
fi

COMMIT_MESSAGE="$1"
shift

echo "=== Batch Commit ==="
echo "Message: $COMMIT_MESSAGE"
echo ""

# Add all specified files (or all if none specified)
if [ $# -eq 0 ]; then
    git add -A
    echo "Staging all changes"
else
    git add "$@"
    echo "Staging: $*"
fi

# Show what's being committed
echo ""
echo "Files to be committed:"
git diff --cached --name-only

# Commit
echo ""
git commit -m "$COMMIT_MESSAGE"

if [ $? -eq 0 ]; then
    echo ""
    echo "=== Commit successful ==="
    echo "Commit: $(git log --oneline -1)"
else
    echo ""
    echo "ERROR: Commit failed"
    exit 1
fi
