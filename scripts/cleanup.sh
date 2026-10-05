#!/bin/bash
# Automated cleanup of temp files and old artifacts.
# Usage: cleanup.sh [project-dir]

set -uo pipefail

PROJECT_DIR="${1:-.}"

echo "=== Cleanup ==="
echo "Project: $PROJECT_DIR"
echo ""

# Remove temp files
echo "Removing temp files..."
find "$PROJECT_DIR" -name "*.tmp" -delete 2>/dev/null || true
find "$PROJECT_DIR" -name "*.bak" -delete 2>/dev/null || true
find "$PROJECT_DIR" -name "*~" -delete 2>/dev/null || true
find "$PROJECT_DIR" -name ".DS_Store" -delete 2>/dev/null || true

# Remove __pycache__ directories
echo "Removing __pycache__..."
find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Remove old log files (> 7 days)
echo "Removing old log files..."
find "$PROJECT_DIR" -name "*.log" -mtime +7 -delete 2>/dev/null || true

# Remove old review outputs (> 30 days)
echo "Removing old review outputs..."
find "$PROJECT_DIR" -name "review-*.txt" -mtime +30 -delete 2>/dev/null || true

# Clean podman build cache (if requested)
if [ "${CLEAN_PODMAN:-0}" = "1" ]; then
    echo "Cleaning podman build cache..."
    podman builder prune -f 2>/dev/null || true
fi

echo ""
echo "=== Cleanup complete ==="
echo "Disk usage:"
df -h / | tail -1
