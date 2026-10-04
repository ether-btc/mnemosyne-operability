#!/usr/bin/env python3
"""Local-only annotation wrapper for Mnemosyne Operability labeling.

Reads case text from stdin, sends it to the local qwen2.5-1.5b model at
127.0.0.1:8099, and writes the model's response to stdout. No other
capabilities: no file writes, no shell execution, no network egress except
to the local model, no credential access.

Isolation properties:
- Runs with python3 -I (isolated mode, no site-packages)
- Only imports stdlib modules (http.client, json, sys)
- Only network connection is to 127.0.0.1:8099
- No subprocess, os.system, or eval/exec
- No file writes (stdout only)
- No environment variable access except PATH (inherited)
"""
import http.client
import json
import sys

MODEL_HOST = "127.0.0.1"
MODEL_PORT = 8099
MODEL_NAME = "qwen2.5-1.5b-instruct-q5_k_m.gguf"
MAX_TOKENS = 2048
TEMPERATURE = 0.0


def extract_json(text):
    """Extract JSON from model output, stripping markdown fences if present."""
    text = text.strip()
    # Strip markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first line (```json or ```)
        lines = lines[1:]
        # Remove last line if it's ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def normalize_label(raw):
    """Normalize model output to the expected schema."""
    # Try to parse as JSON
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return None

    # If it has "label" and "rationale", normalize to expected schema
    if "label" in obj:
        return {
            "eligible": obj.get("label") not in (None, "none", "not_eligible", "false"),
            "expected_capability": obj.get("label") if obj.get("label") not in (None, "none", "not_eligible", "false") else "none",
            "rationale": obj.get("rationale", ""),
        }

    # If it already has the expected fields, pass through
    if "eligible" in obj:
        return obj

    return None


def main():
    # Read case text from stdin
    case_text = sys.stdin.read()
    if not case_text.strip():
        print("ERROR: empty input", file=sys.stderr)
        sys.exit(1)

    # Build the prompt — explicitly forbid markdown fences
    prompt = f"""You are a labeling assistant for a research study on AI agent capability discovery. You will be shown a case and asked to label it according to specific criteria.

IMPORTANT: Respond with ONLY a JSON object. Do NOT use markdown code fences (```). Do NOT add any text before or after the JSON.

Case:
{case_text}

Label the case according to the criteria provided. Respond with JSON only: {{"eligible": true/false, "expected_capability": "<capability name or none>", "rationale": "<brief rationale>"}}"""

    # Send to local model
    try:
        conn = http.client.HTTPConnection(MODEL_HOST, MODEL_PORT, timeout=120)
        body = json.dumps({
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        })
        conn.request("POST", "/v1/chat/completions", body=body, headers={
            "Content-Type": "application/json",
        })
        response = conn.getresponse()
        if response.status != 200:
            print(f"ERROR: model returned {response.status}", file=sys.stderr)
            sys.exit(1)
        result = json.loads(response.read())
        content = result["choices"][0]["message"]["content"]

        # Extract and normalize JSON
        json_text = extract_json(content)
        label = normalize_label(json_text)
        if label is None:
            print(f"ERROR: could not parse label from: {content[:200]}", file=sys.stderr)
            sys.exit(1)

        print(json.dumps(label))
        conn.close()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
