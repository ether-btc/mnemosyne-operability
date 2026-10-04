# Mnemosyne Operability Research

## Purpose
Determine whether Hermes can reduce avoidable user reminders by reliably discovering and using its existing Mnemosyne, wiki, skills, and tools. The target is **just-in-time capability use**, not loading the full inventory into every prompt.

## Status and resume
Research/planning only; **G0 corrective changes locally complete; fresh exact-hash G1 review still pending; no R0 authorized.** Round-2 independent review returned **NO-GO-WITH-CONDITIONS**; raw output and prompt are preserved at `evidence/reviews/round-2/`. Read `STATUS.md` first; the current receipt is `review-state.json`. No R0 execution or session-content access until a fresh exact-hash independent `GO` and privacy/access gate pass.

Run `bash scripts/verify.sh` for the structural project-control check. Run `bash scripts/verify.sh --require-go` to require a fresh exact-hash independent review, one raw GO verdict, a matching `GATE_RECORD_JSON` with no unresolved findings, and the complete manifest; this local gate cannot prove reviewer identity or judgment.

## Scope boundary
Study the operating layer around existing Mnemosyne and Hermes native mechanisms. Preserve Mnemosyne as an upstream dependency. Do not replace/migrate it, build a parallel router, ingest full histories, change live profile/runtime configuration, install software, replay private content externally, commit, or publish as part of this phase.

## Project controls
- [`PRAXIS.md`](PRAXIS.md): problem, unit of analysis, constraints, and outcome.
- [`CODEBOOK.md`](CODEBOOK.md): labels and boundary examples.
- [`METHODOLOGY.md`](METHODOLOGY.md): frozen sampling frame, privacy, blinding, evaluation rules.
- [`ROADMAP.md`](ROADMAP.md): review gate, risk-first tasks, dependencies.
- [`DECISIONS.md`](DECISIONS.md): bot and reviewer dispositions.
- [`STATUS.md`](STATUS.md): current gate and next action.
- [`SOURCES.md`](SOURCES.md): content-hashed local and pinned upstream evidence.
- [`EXECUTION-PROMPT.md`](EXECUTION-PROMPT.md): self-contained continuation contract.
- `review-state.json`: current/prior review receipts. `evidence/reviews/round-1/` and `evidence/reviews/round-2/` preserve each raw prompt/result. The next candidate uses `REVIEW-PROMPT.txt` and `REVIEW-RESULT.txt`.
- `evidence/`: redacted discovery, host-source, session-search contract, and local quality evidence; no private case corpus has been collected.
- `scripts/verify.sh` and `scripts/test_verify.py`: structural check, exact-hash review gate, and black-box regression cases.

## Confidence
**Medium** that the installed stack already offers useful discovery mechanisms; **low** that any new intervention is justified. The cause and frequency of avoidable reminders remain unmeasured. “Do not build” is a valid outcome.
