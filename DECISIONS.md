# Decisions and review dispositions

## Independent review round 1 (2026-10-03)

The reviewer returned **NO-GO-WITH-CONDITIONS**. Its full hash-bound output is `evidence/reviews/round-1/REVIEW-RESULT.txt`; the tool-run artifact was read in full. It recomputed and matched all nine exact hashes before and after inspection. The reviewer did not inspect external repos/services/session databases; external claims are not considered verified by that review.

| Finding | Severity | Disposition | Corrective change / verification gate |
|---|---|---|---|
| F1: “avoidable reminder”/“eligible case” lacks a reproducible rule and denominator; failure-selected corpus can bias the rate. | MAJOR | ADOPT | `PRAXIS.md` defines capability opportunity; `CODEBOOK.md` requires eligibility basis, contemporaneous availability, non-reminder controls, and uncertainty. `METHODOLOGY.md` requires all opportunities in a frozen frame and report of every exclusion. |
| F2: Held-out set can leak because the designer sees all cases before candidate choice. | MAJOR | ADOPT | Freeze separate whole-session/time development and sealed evaluation manifests before intervention design. Reveal evaluation only after candidate/estimator/thresholds are locked; redesign means a fresh holdout. |
| F3: Search coverage/labels/analysis can fail open. | MAJOR | ADOPT | R0 known-positive session-search canary plus profile/index/date coverage receipt. Two blinded local labels per scored case or INCONCLUSIVE, raw agreement/confusion and adjudication disclosed, session-clustered interval and missingness/exclusions preregistered. |
| F4: No retention/access/backup/deletion or inert adversarial-input controls. | MAJOR | ADOPT | `METHODOLOGY.md` sets local-only content boundary, exact private directory/modes, verifies backup/sync exclusion before content access, segregates locators, prohibits external content replay and tools/network in replay, and defines closeout retention/deletion gate. Failure to prove boundaries stops collection. |
| F5: Independent review gate is prose-only; self-disposition or stale bytes can pass. | MAJOR | ADOPT | Every relevant file change invalidates approval. Add machine-readable receipt tied to exact plan file hashes and raw reviewer-output hash; `--require-go` validates receipt, raw result, hashes, exact `VERDICT: GO`, and no unresolved blockers. Integrator cannot self-close blocking findings. Independent review remains required; script is not the reviewer. |
| F6: Prefetch count conflicts; citations mutable/unpreserved. | MINOR | ADOPT | Correct 12,524-char claim to the measurable saved-file size: 10,999 Unicode chars incl. newline, 10,998 excluding, 11,009 bytes; SHA-256 `df4b397a…`. Pin candidate commits, snapshot exact files and licenses, include SHA-256. Remove volatile star/doctor/Mercury details if not load-bearing. |
| F7: Verifier not directly executable and phase-stale; wording overclaims semantics. | MINOR | ADOPT | Make `./scripts/verify.sh` executable; remove fixed “pending/R0” markers; describe default check as structural only; add exact-hash review-receipt mode. Verify the expected NO-GO fails `--require-go`, then fresh GO succeeds only for exact matching files. |

**Review verdict authority:** no corpus collection, session message-content access, intervention, implementation, configuration change, provider replay, or live action until a corrected exact-tree review returns GO. A change to PRAXIS/METHODOLOGY/CODEBOOK/ROADMAP/STATUS/SOURCES/EXECUTION-PROMPT/verifier invalidates any prior review receipt. The next reviewer must independently review changed bytes; this author may propose dispositions but cannot mark review conditions closed on their own.

## Independent review round 2 (2026-10-04)

The reviewer returned **NO-GO-WITH-CONDITIONS** after all 11 frozen file hashes matched before and after review. Raw output and prompt are preserved at `evidence/reviews/round-2/`; round 2 supersedes round-1 prose as the current gate. No session text, database, live configuration, or provider was accessed. Round 2 identified five MAJOR, one MINOR, and one LOW finding:

| Finding | Severity | Disposition | Corrective change / verification |
|---|---|---|---|
| R2-M1: positive-control coverage conflicts with the no-content/provider boundary. | MAJOR | ADOPT | Use the existing `SessionDB.search_messages` method in a local read-only process with `fields=["id", "session_id"]`, private query/expected-ID input, suppressed state logging, and an allowlisted boolean/count output. Do not use the content-bearing `session_search` wrapper. Verify the output contract using synthetic sentinel data before any history canary. R0a must also prove a pinned interpreter path that does not trigger dependency sync/install or Hermes update; otherwise stop. This design is source-verified; no live history call is authorized or performed. |
| R2-M2: label sequence omits the assistant answer/tool trace. | MAJOR | ADOPT | Codebook now has three locked reveal stages: pre-answer evidence; answer/tool trace; then later user turns. Both independent labels and stage-specific evidence are preserved. |
| R2-M3: Roadmap and continuation prompt used conflicting phases/dependencies. | MAJOR | ADOPT | `ROADMAP.md` is the only phase/dependency source. `EXECUTION-PROMPT.md` points to it instead of duplicating numbered steps. Dependency chain is `R0a → R0b → R1 → R2`, with source-only R3 parallel after G1, then `R2 + R3 → R4`. |
| R2-M4: authorized readers, data handoff, non-human labeler isolation, backup/deletion proof underspecified. | MAJOR | ADOPT | Roles and read-only stage-by-stage local handoff are explicit; no broadening file permissions; no non-human labeler unless tools/network/shell/credentials/writes are disabled and a synthetic injection fixture passes. Backup/sync exclusion and deletion receipt requirements are explicit. Any unproven boundary stops collection. |
| R2-M5: raw result could contain contradictory verdicts or mutable receipt-only findings. | MAJOR | ADOPT | `--require-go` requires exactly one `VERDICT: GO` line and one structured `GATE_RECORD_JSON`, cross-checks verdict/findings against the receipt, rejects malformed/duplicate JSON keys and unresolved findings. New black-box tests cover contradictory and duplicate verdicts, malformed and duplicate-key records, and raw unresolved findings. The local verifier does not authenticate reviewer identity or judgment. |
| R2-m6: primary metric wording conflated reminders and omissions. | MINOR | ADOPT | Primary outcome is now avoidable reminder rate; unprompted omissions and task correctness are separately reported. |
| R2-m7: two discovery records are normalized transcriptions, not raw receipts. | LOW | ACCEPT for current gate | They are explicitly labeled as transcriptions and support only “no demonstrated coverage.” Future load-bearing probes require bounded raw receipts that exclude private text and credentials. |

The verdict authorizes no R0 metadata or content access, corpus collection, database read, runtime/provider action, install, deletion, commit, publication, or deployment. Fresh exact-hash independent review is still required after these corrections.

## Consultation and research decisions

| ID | Decision | Basis | Revisit when |
|---|---|---|---|
| D-001 | Diagnose capability discovery/use before changing Mnemosyne storage/core. | Historical closeout reported injection/registration without provider-load failures alongside mistakes; that separates availability from successful use but does not prove a root cause. | Baseline localizes a storage/retrieval defect. |
| D-002 | Define awareness as task-appropriate discovery/correct use, not whole-inventory injection. | Extra context can add cost/noise/privacy risk; no evidence bulk injection improves success. | A registered comparison demonstrates safe benefit. |
| D-003 | Use a full, bounded capability-opportunity frame with non-reminder controls. | Vibe Coding Partner's measurement-first advice adopted; reviewer F1 tightens it. | Coverage or privacy controls fail; then outcome is inconclusive. |
| D-004 | Candidate repositories are study-only, not dependencies/providers. | Exact pins below; GBrain offers a resolver pattern; Agentmemory describes a separate memory server/MCP/hooks. Existing Mnemosyne and Hermes native mechanisms remain the baseline. | Verified gap plus comparative advantage and separate authorization. |
| D-005 | Reject Technical Cofounder's unverified H1–H5 diagnoses and fixed 20-trial/+30-point/top-k/150-LOC/two-week/hook-path assumptions. | They were not derived from source or baseline. Disable-prefetch proposal would perturb live behavior. | Evidence/source verifies a hypothesis and thresholds are preregistered. |
| D-006 | Reject “assembled before API call means local.” | Any context included in an external provider request is sent to that provider. | No revisit; data boundary must match actual egress. |
| D-007 | Do not diagnose context overflow, weak skill matching, or stale memory from symptoms. | No prompt-token loss trace or adjudicated denominator. | Source-backed trace or controlled comparison. |
| D-008 | Keep no-build/inconclusive terminal outcomes. | No causal frequency estimate yet; a new router could add maintenance without benefit. | No revisit. |
| D-009 | The installed Hermes already has a native progressive Tool Search path configured. Test that first; do not add a parallel router by assumption. | Read-only host config: `enabled=auto`, curated deferral includes `session_search`; local source at pinned HEAD documents bridge activation and skill index. `memory.provider=mnemosyne`. Native support does not prove this agent invokes it correctly. | Measured omission class shows a native-path limitation. |
| D-010 | Scope the primary rate to the fixed September 2026 default-profile source frame; do not imply that every task is eligible or that the full census will necessarily be labeled. | The source frame is outcome-independent. Eligibility and any metadata-defined deterministic sample are applied under `CODEBOOK.md`/`METHODOLOGY.md`; generalization is limited to the observed frame/sample. | A separately preregistered prospective observation is authorized. |

## Candidate-repo provenance and verdicts

- **GBrain `garrytan/gbrain`: REFERENCE (study-only).** `master` resolved by `git ls-remote` on 2026-10-03 to `109b992172e1f49107f9de9841758c1d043a2668`. The pinned `skills/RESOLVER.md` has explicit trigger→skill mappings, frontmatter routing signals, and “read before acting” guidance. Its install guide describes a Bun/TypeScript runtime. Exact relevant files and licenses are preserved under `evidence/upstream/` with SHA-256 in `SOURCES.md`. Not installed.
- **Agentmemory `rohitg00/agentmemory`: AVOID as replacement; REFERENCE only.** `main` resolved by `git ls-remote` on 2026-10-03 to `2a00e7b38fc4ae4e38af4134586be0bbe9612706`. Its pinned Hermes README describes a separate service, MCP tools, and six lifecycle hooks. This duplicates the installed memory-provider role absent proof of a gap. Exact integration README and license are preserved with SHA-256 in `evidence/upstream/`. Not installed.

## Hermes integration facts (host-pinned)

- Host CLI observed 2026-10-03: v0.21.5+4699.g5f666db; repository HEAD `5f666db4e3af17142fa62b11e06ff377d5239a42`; clean `git status --short`; local code reports an upstream tip and commit gap. This is a version-provenance fact, **not** permission or recommendation to update.
- Local `tools/tool_search.py` and `agent/prompt_builder.py` at that HEAD demonstrate built-in dynamic tool discovery and skill-index/availability filtering. Read-only config sets `tools.tool_search.enabled=auto` and `memory.provider=mnemosyne`. Exact file hashes and line ranges are in `SOURCES.md`.
- Current web docs are a supplementary design reference only; exact host behavior is pinned to local source/config. No runtime mutation performed.

## G0 verifier decision

- **D-011:** Extend `scripts/verify.sh` with an exact-hash `--require-go` mode and black-box tests instead of adding a separate validator. The gate now requires exactly one raw `VERDICT: GO` line plus exactly one `GATE_RECORD_JSON` containing `verdict` and `unresolved_findings`; it rejects duplicate verdicts/JSON keys, malformed records, raw/receipt disagreement, unresolved findings, stale files, and mismatched prompt manifests. It cannot authenticate reviewer identity/independence or plan truth. The independent reviewer remains the gate. The hash-bound set covers 18 plan, verifier, test, and supporting-evidence files. `scripts/test_verify.py` has 18 black-box cases (verify on this tree); structural mode remains structural only, and the preserved round-2 NO-GO must fail `--require-go`.

## G0 partner-review dispositions (v2) — D-012

| Finding | Severity | Disposition | Action / remaining limit |
|---|---|---|---|
| V-G0-M1: R0b did not specify containment of every child-output channel. | MAJOR | ADOPT | `METHODOLOGY.md` now requires the exact child launcher to close inherited descriptors, capture stdout/stderr in memory, suppress logging/warnings before imports, never persist/log/forward child bytes, allowlist the only returned JSON record, and audit for file/syslog/socket/network sinks. A sentinel fixture must exercise the actual launcher and all channels. This is a plan contract, not a runtime proof; any unproven sink keeps R0b `INCOMPLETE`. |
| V-G0-m1: “failure stages” conflated causal classification with label-reveal order. | MINOR | ADOPT | `PRAXIS.md` calls these C1–C5 failure categories and maps C1–C2 to Codebook Stage 1, C3–C5 to Stage 2, with Stage 3 reserved for follow-up/reminder outcomes. `CODEBOOK.md` explicitly labels reveal stages. |
| V-G0-m2: no tests for malformed-but-valid gate-record field types or invalid receipt JSON. | MINOR | ADOPT | Added black-box wrong-type `unresolved_findings` and malformed `review-state.json` tests. The current verifier already fails these inputs; the new cases lock that behavior. |
| V-G0-l1: README status phrasing did not match the exact STATUS gate. | LOW | ADOPT | README now says “G0 corrections in progress; no R0 authorized.” |

Technical Cofounder v2 read all 13 requested files and returned CLEAR; no additional findings. Both bot audits are advisory only and do not close the round-2 formal NO-GO.

## Mercury Decide steering (2026-10-04) — D-013

The free build `inception/mercury-decide-20260930` was queried through the verified Decisions API. Its `choice` distribution selected “apply the smallest corrections, verify locally, checkpoint G0, then pause before fresh independent review” (0.999336); alternatives were submit current tree unchanged (0.000626) and close immediately as inconclusive/no-build (0.000038). These are framing-sensitive steering scores, not calibrated probabilities or authorization. A matched affirmative probe about submitting unchanged now scored 0.002473 with the actual findings versus 0.001810 under a no-findings counterfactual (Δ=0.000662), too small to treat as a useful discriminator. The selected course follows the independently observed audit findings and existing review gate, not model confidence. Procedure follows `mercury-decide-oracle` and the verified use recorded in `/home/hermes-pi/wiki/projects/aeon-upstream-rebase-2026-10-04.md`.


