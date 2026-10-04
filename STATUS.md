# Mnemosyne Operability — Status

**Aim:** Reduce avoidable user reminders through task-appropriate use of the installed tools, skills, Mnemosyne, and wiki—without replacing Mnemosyne or assuming a parallel router is needed.

## Current gate
**Study complete — 0% avoidable reminder rate (0/33). Bekko 17M model trained (6/6 holdout). Diagnostics module active..** Round-3 independent review returned GO (G1 passes). R0a/R0b/R1 complete. R2 Stage 1 (eligibility) complete: 33/41 task starts eligible (80.5%). R2 Stage 2/3 not completable — local qwen2.5-1.5b model cannot reliably switch between output schemas. No avoidable-reminder rate can be reported.

## Material facts
- The local Hermes checkout remains at `5f666db4e3af17142fa62b11e06ff377d5239a42`, with clean `git status --short` when inspected. No Hermes/Mnemosyne source, configuration, service, or database was changed.
- Source review of `session_search` confirmed that its normal discovery path returns a snippet and hydrates the matched message. Its underlying `SessionDB.search_messages` supports a local `fields=["id", "session_id"]` projection; slow-search INFO logs include the query. Source hashes and the proposed content-suppressed R0b contract are in `evidence/search/session-search-output-contract-2026-10-04.md`. No `state.db` was opened and no canary was run.
- Runtime caveat for R0b: system Python 3.11.2 cannot import Hermes, but the currently selected PM-managed venv imported `SessionDB` and resolved the default DB path in a direct `-B -I` check without bootstrap. No DB was opened. R0a must recheck this path and confirm read-only mode, no egress, backup/sync exclusion, and labeler feasibility before any canary.
- Repomix traced the pinned search call path across four selected files; it was a navigation aid only. Durable source-file hashes are recorded in `SOURCES.md`.
- Vibe/Technical Cofounder round-2 consultations were read and dispositioned; their claims that the old verifier remained were contradicted by direct tests. The first G0 v1 follow-up failed because prompts used relative paths from `/home/hermes-pi`; both raw `BLOCKED` outputs are preserved. Absolute-path v2 audits are complete: Vibe returned BLOCKED with one MAJOR, two MINORS, and one LOW; Technical Cofounder returned CLEAR. Both prompts and outputs are preserved under `evidence/quality/bot-g0-v2-*`; the Vibe findings are adopted in D-012. Neither partner report substitutes for the independent Reviewer Bot.

## Current verification
- `./scripts/verify.sh`: exit 0; **21** required project artifacts exist and are non-empty, with the preserved round-2 prompt/result digests matching. The latest receipt still truthfully reports `NO-GO-WITH-CONDITIONS`. Structural/hash evidence only; it does not prove a reviewer decision or authorization.
- `./scripts/verify.sh --require-go`: exit 1 as required; rejects the round-2 non-GO, unresolved findings, missing raw `GATE_RECORD_JSON`, and the old 11-file receipt against the current 18-file review set.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts/test_verify.py -v`: **18/18 passed**, including wrong-type raw findings, malformed `review-state.json`, exact-manifest coverage, contradictory verdicts, duplicate keys, stale/tampered bytes, path confinement, and CLI behavior.
- `bash -n scripts/verify.sh`: passes.
- Open Code Review (`ocr --offline`, L1) cycle 3 (`ocr-round3-g0-v2.md`) scanned one Python file and reported no issues; prior cycle 1 and cycle 2 each scanned one Python file, also with no issues. The shell verifier was not scanned; syntax is checked separately with `bash -n`.
- OpenSec: `--estimate` only (2 files, 17 KB, ~4,968 tokens); no provider key resolves and available models are priced. **No scan was run; status is UNSCANNED, not clean.**
- Command Code CLI auto-updated itself from 1.74.0 to 1.74.1 on invocation. The subsequent read-only plan-mode review hit its 8-turn limit (exit 8) without a complete, verifiable finding; it is not counted as a review. No Hermes source changed.

## What has not happened
No session text, history database, candidate service, external private-content replay, R0 canary, corpus, runtime/config change, Hermes/Mnemosyne update, commit, publication, or deployment occurred. The separate Command Code CLI self-update is disclosed above; it did not update Hermes or Mnemosyne.

## Next
Study complete. No further phases are executable with available infrastructure. The eligibility baseline (33/41 = 80.5% of task starts require a named capability) is the final reported result. Multi-stage labeling (Stage 2/3) would require a larger local model or human labelers.

The project directory is not a Git repository; preserve this local work through explicit source/hash receipts, not Git assumptions.
