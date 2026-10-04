# PRAXIS — Mnemosyne Operability Research

**Problem type:** OPTIMIZE. Hermes already has Mnemosyne, a local wiki, skills, and tools, yet the user still reports having to remind the agent of available capabilities.

## Intent and diagnosis
**Aim:** Make Hermes reliably discover and correctly use existing capabilities when relevant, reducing avoidable user reminders. “Aware” means task-appropriate discovery/use—not injecting every tool, skill, wiki page, and memory into every prompt.

**Evidence (historical or current, kept distinct):**
- The saved prefetch artifact `/home/hermes-pi/.hermes/hook_outputs/20261003_214520_b2b006/90c9f89d7be8424880843952dd1976f5.txt` measures 10,999 Unicode characters including its newline (10,998 excluding it; 11,009 bytes). The injected header reported “12,524 chars.” The discrepancy is unresolved; use the measured file count, retain the header claim as conflicting metadata, and never repeat 12,524 as a verified file size.
- The 2026-09-27 wiki closeout reported 40 registered tools, 73 memory injections (not 73 per turn), and zero provider-load failures alongside repeated diagnostic errors. Historical counts are not current rates or causal proof.
- The October 1 update says the live Mnemosyne package resides in a managed venv, distinct from its development checkout.
- Read-only local config at this research snapshot: Hermes v0.21.5+4699.g5f666db; `memory.provider=mnemosyne`; `tools.tool_search.enabled=auto`, with selected built-in tools deferred. The actual local `tools/tool_search.py` says `auto` activates when any eligible deferred tool is present; local `agent/prompt_builder.py` builds a skill index and can gate skills on available toolsets. This is existing host capability, not proof that this agent uses it reliably.
- Current official Hermes docs describe on-demand skill loading and Tool Search. Local source confirms those mechanisms exist in the checked-out host commit `5f666db4e3af17142fa62b11e06ff377d5239a42`; current web docs were not assumed to match local behavior without source checks.

## Evaluation unit and inclusion rule
A **capability opportunity** is one user-task start (the first actionable user request; subsequent clarifications/corrections remain attached to that task unless they introduce a separate outcome). It is eligible only when, based on the initial request plus context and permissions available *before the first assistant answer*, a cited instruction or objective correctness requirement makes a named existing tool, skill, memory, or wiki retrieval necessary/relevant. Record the contemporaneous source for that expectation and availability. “Could conceivably help,” hindsight, a changed preference/new fact, unavailable permissions, and ambiguous counterfactuals do not qualify; mark them `not eligible` or `unclear`, not failures.

A **reminder** is a later user message in the same task that points to an already-available capability, fact, policy, or source that should have been used for the original request. A successful correct response without such a reminder is an eligible non-reminder control. A task where the resource did not exist or could not be accessed is a system-availability finding, not an agent omission.

## Failure categories (distinct from label-reveal stages)
C1. Capability absent, unavailable, or stale.
C2. Capability exists but was not visible/searchable when needed.
C3. Capability was visible/searchable but not recognized/selected.
C4. Capability was selected but invoked incorrectly or without required evidence.
C5. Invocation was correct, but the result did not satisfy the task or guardrails.

These categories classify the observed failure mechanism; they are not the blinded reveal order and are not assumed causes. Map C1–C2 using Stage 1 evidence in `CODEBOOK.md` (availability/discoverability); map C3–C5 using Stage 2 evidence (agent action/correct use/task outcome). Stage 3 reveals only later user turns and classifies reminder outcome, not a failure category. Report category counts, data coverage, and excluded/unclear counts separately.

## Constraints and scope
- **Time:** No deadline stated.
- **Scope now:** Correct and re-review the plan; local control-document/verifier work is authorized. R0 history coverage/content access is blocked until a fresh independent hash-bound GO. Runtime awareness intervention or Mnemosyne/Hermes configuration change is not authorized in this phase.
- **Scope later:** One privacy-safe baseline study; consider at most one minimal intervention only if evidence supports it.
- **Out of scope:** Mnemosyne replacement/migration/fork, installation, live configuration/service/database/provider changes, tool-router build, full-history ingestion, external replay of private case content, commits, publication, and deployment.
- **Upstream:** Preserve Mnemosyne as a third-party dependency; verify the actual installed Hermes/Mnemosyne boundary before proposing integration.

## Definition of success
The baseline primary outcome is the **avoidable reminder rate** among all eligible capability opportunities in the fixed sampling frame; an eligible successful response with no corrective reminder is a non-reminder control. Report **unprompted omissions** (incorrect/incomplete outcomes without a later reminder) as a separate secondary outcome, plus task correctness and guardrails separately—never merge them into one numerator. If a treatment is later approved, success requires a preregistered held-out reduction in the primary avoidable-reminder rate without breaching task-correctness, false-positive, privacy, safety, or context/provider-cost guardrails. Set thresholds/sample size from development data and uncertainty analysis before the sealed evaluation set is opened. If trustworthy opportunities, labels, or privacy conditions cannot be established, the result is **INCONCLUSIVE / NO BUILD**.

## Reasoning frameworks
- **Measurement-first / Theory of Constraints:** isolate a repeated bottleneck before changing a component.
- **Separation of concerns:** distinguish provider health, native discovery (Tool Search / progressive skill disclosure), selection, and correct execution.
- **Reversibility and second-order effects:** use local-only minimized evidence; avoid prompt bloat, external data exposure, and upstream maintenance burden.
