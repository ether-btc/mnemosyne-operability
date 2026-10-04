# Continuation Prompt — Mnemosyne Operability

## Role and aim
You are the Hermes default-profile integrator. Determine whether task-appropriate discovery and correct use of existing tools, skills, Mnemosyne, and wiki can measurably reduce avoidable user reminders—without replacing Mnemosyne, adding a parallel router, or creating upstream-maintenance burden. `NO BUILD` and `INCONCLUSIVE` are valid outcomes. Awareness is just-in-time discovery/use, not full-inventory prompt stuffing.

## Resume
Project: `/home/hermes-pi/projects/mnemosyne-operability/`.
1. Read `STATUS.md`, `DECISIONS.md`, `PRAXIS.md`, `CODEBOOK.md`, `METHODOLOGY.md`, `ROADMAP.md`, `SOURCES.md`, and `review-state.json`.
2. Read `evidence/reviews/round-2/REVIEW-RESULT.txt` and confirm its digest against `review-state.json`; round 2 is `NO-GO-WITH-CONDITIONS`. Round-1 evidence is preserved in `evidence/reviews/round-1/`.
3. Run `bash scripts/verify.sh`, `bash scripts/verify.sh --require-go`, `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts/test_verify.py -v`, and `bash -n scripts/verify.sh`.
4. G0 corrective changes are locally complete. Verify the prepared candidate prompt and 18-file manifest under `evidence/reviews/round-3/`, then submit that exact tree for fresh independent review. Do not begin R0 or read session message text until fresh independent GO.

## Source of truth and current status
`ROADMAP.md` owns every phase name, ordering, dependency, and done criterion; do not reproduce a second numbered workflow here. `METHODOLOGY.md` and `CODEBOOK.md` own the measurement, three-stage label reveal, and data boundary. `SOURCES.md` owns pinned local/upstream evidence. `review-state.json` is a mutable receipt, not reviewer authentication or authorization.

The round-2 reviewer identified five MAJOR findings (R0 positive-control privacy path; missing assistant-answer label stage; conflicting phase/dependency graph; reader/labeler isolation; verifier acceptance of contradictory/malformed raw results) and two non-major findings (one MINOR on metric terminology; one LOW on discovery-record provenance). All have dispositions and are incorporated in the current G0 candidate; the Vibe v2 advisory findings are also dispositioned in D-012. This does not grant R0 or supersede the NO-GO gate. Any change to these files invalidates a future exact-hash review.

## Hard gates
- No history text or corpus access until a fresh independent exact-hash `GO` and R0a metadata/privacy checks. R0a must prove a pinned runtime/import path that does not invoke dependency sync, installation, or Hermes update; if unavailable, stop for separate authorization. R0b, only after R0a, uses a disposable local `SessionDB.search_messages` child with `fields=["id", "session_id"]`, a private input manifest, closed inherited descriptors, and a tested wrapper that captures stdout/stderr and returns only the allowlisted boolean/count receipt. It must not log, persist, forward, or expose raw child output; audit for file/syslog/socket/network sinks and stop `INCOMPLETE` if any cannot be excluded. The synthetic sentinel fixture must exercise the exact launcher/wrapper before any canary. Never send private content to the normal assistant tool, external models, bots, RepoHunt, or candidate services.
- If reader roles, two independent data-safe local labelers, backup/sync exclusion, provider egress, or a content-suppressed R0b path cannot be proven, stop as `INCOMPLETE`; do not weaken the boundary.
- No implementation, runtime/config/database/provider change, installation, publication, commit, deployment, or live treatment without its distinct authorization. Before any live Hermes update on the RPi5, announce and wait for the user.
- Independent review informs but does not authorize later gates. Preserve complete raw outputs and exact hashes. Any reviewed-file change invalidates that review.

**Resume trigger:** “Resume Mnemosyne Operability at `/home/hermes-pi/projects/mnemosyne-operability/STATUS.md`. Read the complete round-2 NO-GO result and project controls, verify the prepared round-3 exact-hash candidate prompt/manifest, and obtain the fresh independent G1 review. Do not begin R0 or access session text until the new reviewer returns GO.”
