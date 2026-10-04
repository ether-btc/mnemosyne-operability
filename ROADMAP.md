# Roadmap — risk-first research

**Study complete — limited result.** Round-3 independent review returned GO. R0a/R0b/R1 complete. R2 Stage 1 (eligibility) complete: 33/41 task starts eligible (80.5%). R2 Stage 2/3 not completable with available local model (qwen2.5-1.5b cannot switch output schemas). No avoidable-reminder rate reported.

**Riskiest assumption:** reported reminders reflect a recurring, actionable capability-use failure rather than changed intent, unavailable access, or isolated reasoning mistakes. `INCONCLUSIVE` and `NO BUILD` remain valid terminal outcomes.

## Tasks

| ID | Task | Depends on | Done when |
|---|---|---|---|
| G0 | Correct the round-2 findings in the canonical plan, codebook, source map, and verifier. | Round-2 result | Every finding is dispositioned; structural check and regression tests pass; exact revised hashes are frozen; no history content is accessed. |
| G1 | Fresh independent review of exact G0 bytes. | G0 | Reviewer returns one authoritative `VERDICT: GO`, `GATE_RECORD_JSON` has `unresolved_findings: []`, exact prompt/result/file hashes match, and the verifier accepts. Any reviewed-file change invalidates it. |
| R0a | Metadata-only preflight: source/profile/schema/date/index counts; confirm a pinned Python/SessionDB import path that cannot trigger dependency sync/install or Hermes update; verify read-only mode, transport/egress, backup/sync exclusion, reader roles, two labelers, and the synthetic leakage-test path. No session text. | G1 | Each boundary has exact local evidence; unknowns stop the study before the canary. |
| R0b | Run the non-scored, local positive control through `SessionDB.search_messages` with metadata-only result projection. | R0a | The exact child launcher closes inherited descriptors and captures stdout/stderr; a synthetic sentinel fixture exercises the same wrapper and verifies no raw values escape and only the allowlisted receipt can be returned. R0a proves no additional file/network/descriptor sink and DB read-only mode. The receipt proves the expected hit without text/IDs leaving the local process; any unproven sink, leak, or missing hit is `INCOMPLETE`. |
| R1 | Freeze the September 2026 default-profile session universe, whole-session/time development/evaluation manifests, and any metadata-based session-sampling rule. After the split, identify every task start within sampled sessions and retain all non-reminder controls. | R0b | Session IDs, split, and sampling/denominator rules are hashed before text/outcomes are reviewed; no FTS-hit or reminder-only selection. |
| R2 | Apply `CODEBOOK.md` to all sampled eligible and non-reminder opportunities through the three locked label stages. | R1; privacy, access, and retention gates | Counts, exclusions, raw double-label agreement, disagreement/adjudication, and uncertainty are reported. If two safe local labelers cannot participate, stop as `INCONCLUSIVE`. |
| R3 | Map the installed native path: Tool Search, skill disclosure, Mnemosyne prefetch, wiki lookup, and available telemetry. Pinned candidate repositories remain reference-only. | G1; may run alongside R0a using source/metadata only | Configured, discoverable, invoked, and correctly used are distinguished; no historical content is opened. |
| R4 | If R2/R3 support a treatment, lock the hypothesis, estimator, guardrails, privacy limits, and sealed evaluation procedure; obtain fresh independent review. | R2 + R3 | Exact-hash GO; no treatment or external/provider action without separate authorization. |
| R5 | Conditional held-out comparison on an uncontaminated whole-session/time partition. | R4 and separate authorization for any live/provider action | Full denominator and guardrails reported; otherwise reject or mark inconclusive. |
| R6 | Conditional smallest reversible implementation only if measured results justify it. | R5; separate implementation authorization and exact-tree review | Tests, rollback, and upstream-update compatibility verified; publication/live activation remains separately gated. |

## Dependencies

`G0 → G1 → R0a → R0b → R1 → R2`; `G1 → R3` (source-only/metadata-only; it may run in parallel with R0a). Then `R2 + R3 → R4 → R5 → R6`. No numbered phase is duplicated in `EXECUTION-PROMPT.md`; this file is the phase source of truth. R0b is the sole bounded local text-query control; broader history/case access remains gated by R0a/R0b and any separate required authorization.

## Decision milestones

- **M0 — Plan trustworthy:** round-2 conditions closed and exact-tree independent GO.
- **M1 — Coverage/privacy proven:** metadata preflight and content-suppressed positive control pass.
- **M2 — Baseline measurable:** all eligible and non-reminder controls labeled with disagreements visible.
- **M3 — Existing path understood:** host-pinned native mechanisms assessed before proposing new layers.
- **M4 — Build decision defensible:** no-build or one registered candidate with sealed evaluation.
- **M5 — Effect or rejection demonstrated:** authorized held-out comparison meets all registered criteria, or is rejected/inconclusive.

A passing documentation verifier, historical incident, healthy provider, candidate-repository feature, or Mercury Decide vote is not proof that Hermes is more aware or that a new component should be built.
