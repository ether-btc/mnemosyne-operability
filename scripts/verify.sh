#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-}"
if [[ "$#" -gt 1 || ( -n "$MODE" && "$MODE" != "--require-go" ) ]]; then
  printf 'Usage: %s [--require-go]\n' "$0" >&2
  exit 2
fi
python3 - "$ROOT" "$MODE" <<'PY'
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
require_go = sys.argv[2] == "--require-go"
reviewed = (
    "README.md", "PRAXIS.md", "METHODOLOGY.md", "CODEBOOK.md", "ROADMAP.md",
    "DECISIONS.md", "STATUS.md", "SOURCES.md", "EXECUTION-PROMPT.md",
    "scripts/verify.sh", "scripts/test_verify.py",
    "evidence/search/session-search-output-contract-2026-10-04.md",
    "evidence/quality/local-tool-checks-2026-10-04.md",
    "evidence/quality/bot-g0-v2-vibe-prompt.txt",
    "evidence/quality/bot-g0-v2-vibe-review.txt",
    "evidence/quality/bot-g0-v2-cofounder-prompt.txt",
    "evidence/quality/bot-g0-v2-cofounder-review.txt",
    "evidence/quality/ocr-round3-g0-v2.md",
)
required = reviewed + ("REVIEW-PROMPT.txt", "REVIEW-RESULT.txt", "review-state.json")
errors = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique_object(pairs):
    record = {}
    for key, value in pairs:
        if key in record:
            raise ValueError("duplicate JSON key")
        record[key] = value
    return record


def project_file(value):
    candidate = root / value
    try:
        path = candidate.resolve(strict=True)
    except OSError:
        return None
    if root not in path.parents or not path.is_file():
        return None
    return path


def confined_file(value, label):
    if not isinstance(value, str) or not value or Path(value).is_absolute() or ".." in Path(value).parts:
        errors.append(f"invalid {label} path")
        return None
    path = (root / value).resolve()
    if root not in path.parents or not path.is_file():
        errors.append(f"missing or out-of-project {label}: {value}")
        return None
    return path

for rel in required:
    path = project_file(rel)
    if path is None or path.stat().st_size == 0:
        errors.append(f"missing or empty required artifact: {rel}")

receipt_path = root / "review-state.json"
receipt = None
if receipt_path.is_file():
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid review-state.json: {exc}")

review = receipt.get("latest_review") if isinstance(receipt, dict) else None
if not isinstance(review, dict):
    errors.append("review-state.json has no latest_review record")
else:
    result_path = confined_file(review.get("result_path"), "review result")
    prompt_path = confined_file(review.get("prompt_path"), "review prompt")
    for path, key, label in (
        (result_path, "result_sha256", "review result"),
        (prompt_path, "prompt_sha256", "review prompt"),
    ):
        if path is not None and review.get(key) != digest(path):
            errors.append(f"{label} digest mismatch")

if errors:
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"PASS: {len(required)} required project artifacts exist and are non-empty.")
print("PASS: recorded raw review and prompt digests match their files.")
print(f"PLAN REVIEW: {review.get('verdict', 'UNKNOWN')} (round {review.get('round', 'UNKNOWN')}).")
print("LIMIT: structural/hash consistency only; it cannot establish reviewer identity, independence, plan truth, or authorization.")

if not require_go:
    raise SystemExit(0)

if receipt.get("schema_version") != 2:
    errors.append("--require-go needs review-state schema_version 2")
if review.get("verdict") != "GO":
    errors.append("latest review receipt is not exact GO")
if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
    errors.append("reviewer attribution is missing")
if not isinstance(review.get("round"), int) or review["round"] < 2:
    errors.append("a fresh review after round 1 is required")
if review.get("unresolved_findings") != []:
    errors.append("unresolved_findings must be an explicit empty list")
prompt_path = confined_file(review.get("prompt_path"), "review prompt")
files = review.get("reviewed_files")
if isinstance(files, dict) and prompt_path is not None:
    prompt_text = prompt_path.read_text(encoding="utf-8", errors="replace")
    rows = []
    for line in prompt_text.splitlines():
        fields = line.split("  ", 1)
        if len(fields) == 2 and re.fullmatch(r"[0-9a-f]{64}", fields[0]):
            rows.append((fields[0], fields[1]))
    prompt_files = {rel: sha for sha, rel in rows}
    if len(prompt_files) != len(rows) or prompt_files != files:
        errors.append("review prompt's exact-hash manifest does not match the receipt")
result_path = confined_file(review.get("result_path"), "review result")
if result_path is not None:
    result_text = result_path.read_text(encoding="utf-8", errors="replace")
    verdict_lines = [line.partition(":")[2].strip() for line in result_text.splitlines()
                     if line.startswith("VERDICT:")]
    if verdict_lines != ["GO"]:
        errors.append("raw review must contain exactly one authoritative VERDICT: GO line")
    record_lines = [line.partition(":")[2].strip() for line in result_text.splitlines()
                    if line.startswith("GATE_RECORD_JSON:")]
    if len(record_lines) != 1:
        errors.append("raw review must contain exactly one GATE_RECORD_JSON line")
    else:
        try:
            record = json.loads(record_lines[0], object_pairs_hook=unique_object)
        except (json.JSONDecodeError, ValueError):
            errors.append("raw review GATE_RECORD_JSON is malformed or has duplicate keys")
        else:
            if not isinstance(record, dict):
                errors.append("raw review GATE_RECORD_JSON must be an object")
            else:
                if set(record) != {"verdict", "unresolved_findings"}:
                    errors.append("raw review GATE_RECORD_JSON has unexpected or missing fields")
                if record.get("verdict") != review.get("verdict"):
                    errors.append("raw review gate record disagrees with receipt verdict")
                if record.get("unresolved_findings") != review.get("unresolved_findings"):
                    errors.append("raw review findings disagree with receipt")
                if record.get("unresolved_findings") != []:
                    errors.append("raw review declares unresolved findings")
if not isinstance(files, dict) or set(files) != set(reviewed):
    errors.append("reviewed_files must exactly cover the required plan, verifier, test, and evidence files")
else:
    for rel in reviewed:
        path = project_file(rel)
        expected = files.get(rel)
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            errors.append(f"invalid SHA-256 receipt for {rel}")
        elif path is None or digest(path) != expected:
            errors.append(f"reviewed file changed or missing: {rel}")
if errors:
    for error in errors:
        print(f"BLOCKED: {error}", file=sys.stderr)
    raise SystemExit(1)
print("PASS: recorded GO receipt's exact-hash manifest matches current files.")
PY
