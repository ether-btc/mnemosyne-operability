# Sources and evidence register

**Snapshot:** 2026-10-04. External URLs, local file paths, revision/content hashes, and measurement provenance are recorded below. Local wiki counts are historical, not present-state invariants.

## Local primary records

1. `/home/hermes-pi/wiki/continue/mnemosyne-ops-closeout-2026-09-27.md`, SHA-256 `3da4de14eef310337911a1bf0a1136c33179de31a2bd765bec8ccea6f229f461`. Lines 55–58 report historical 40 tools, 73 memory injections (not per turn), and zero provider failures; §§2/8c/9 record the separate managed install/dev-checkout boundary.
2. `/home/hermes-pi/wiki/audits/mnemosyne-upstream-update-2026-10-01.md`, SHA-256 `79cd12ba46dbd915095df9a49e6ecff92ab7268beae6be5e79723df0722820b6`. Lines 18–27 establish the live managed venv is not the development checkout.
3. `/home/hermes-pi/wiki/systems/memory-and-mnemosyne.md`, SHA-256 `a593aa65cf8035fc4e217ada4d7a97212af05ab5763439436ddbbbf5d7fb74be`; frontmatter last updated 2026-08-07. Old version/config numbers treated as historical pending reconciliation.
4. Prefetch artifact `/home/hermes-pi/.hermes/hook_outputs/20261003_214520_b2b006/90c9f89d7be8424880843952dd1976f5.txt`, SHA-256 `df4b397abb1ac69613e354e33848fc4deb32c84fa237803b335ba7624d4b4df2`: 11,009 bytes; 10,999 Unicode chars including final newline; 10,998 excluding newline. Injected metadata said “12,524 chars”; mismatch unexplained, so only file measurement is used. It is contextual evidence, not an evaluation corpus.
5. Read-only history search probes are summarized (not raw DB contents) in `evidence/search/session-search-probes-2026-10-03.md`; each returned `count=0`, `sessions_searched=0`. This proves no corpus coverage and is not a negative finding.
6. RepoHunt query terms and pinned follow-up are transcribed in `evidence/search/repohunt-discovery-2026-10-03.md`; this is not the raw MCP JSON response. The direct `git ls-remote` refs are pinned and relevant source snapshots/license bytes are preserved below.
7. Host version/config/source observation and exact commands are preserved in `evidence/host-config-2026-10-03.md`.

## Hermes native capability mechanism — pinned host source

The local repository was `/home/hermes-pi/.hermes/hermes-agent`, HEAD `5f666db4e3af17142fa62b11e06ff377d5239a42` (2026-09-29), `git status --short` empty at observation. CLI reported v0.21.5+4699.g5f666db and a 1,527-commit update gap; this is not an update authorization.

- `tools/tool_search.py`, SHA-256 `a0728e9f889eaa30e118e4d027cb51e677a935c2227e819a37be2bd648054099`, lines 1–7, 197–206, 231–265: deferred tools route through `tool_search`/`tool_describe`/`tool_call`; `auto` activates when a deferrable tool exists; the bridge tells the model to search rather than claim a deferred capability is unavailable.
- `agent/prompt_builder.py`, SHA-256 `2acbf9a8cf8ba480614f2fccf8281b7bbd2748c040cd742820634bf382424319`, lines 1261–1280 and 1294–1319: skill display is filtered against available tools/toolsets and a skill index is assembled.
- `agent/memory_provider.py`, SHA-256 `a4e44a293013fff831ac136ab77c556541cd18817f53bd662e97090cd80bd5a6`, lines 1–5, 116–123: one external provider at a time; `system_prompt_block()` is static while `prefetch()` is per upcoming turn.
- Read-only config in `evidence/host-config-2026-10-03.md`: `memory.provider=mnemosyne`; Tool Search enabled `auto`, `defer` includes `session_search` and selected auxiliary tools.

## Native session-search output contract — same pinned host

The actual source hashes, call path, and privacy-relevant behavior are documented in `evidence/search/session-search-output-contract-2026-10-04.md`. `session_search` returns snippets and hydrates matched messages, so it cannot be invoked through the provider-bound assistant tool for the R0 positive control. The lower-level `SessionDB.search_messages` supports `fields=["id", "session_id"]`; the source finalizer removes full message content and projects only requested fields, while slow-search INFO logs include the query. This supports a local, read-only, output-contained R0b design only if the wrapper captures every child output channel and R0a proves there are no additional file/network/descriptor sinks; **no database was opened and no canary ran**. System Python 3.11.2 cannot import Hermes, but the currently selected PM-managed venv did import `SessionDB` and resolve the default DB path through a direct `-B -I` import-only check that bypassed `hermes_bootstrap`; full command/result and limits are in the evidence note. Recheck that path at R0a. This is not evidence of live index/profile coverage or backup/provider safety.

## Local review-tool scope

`evidence/quality/local-tool-checks-2026-10-04.md` records tool operations and boundaries. Open Code Review/OCR L1 cycles 1–3 each scanned one Python file only; all three reported no issues, and the shell wrapper was not scanned. The cycle-3 report `evidence/quality/ocr-round3-g0-v2.md` has SHA-256 `17486bc4d444b56b9c452d14d71b0b88a95c7a0fb7f8fb4f49d1d98fa42eee62`. OpenSec was **UNSCANNED**: estimate only (2 files/17 KB/~4,968 tokens), no provider key resolves, all available models are priced. Command Code CLI did not return a complete review; it auto-updated itself from 1.74.0 to 1.74.1 and exited 8 at the configured turn limit. The first G0 Vibe/Cofounder consultation attempt was blocked by relative-path lookup from `/home/hermes-pi`; exact failures are preserved in the quality directory. Corrected v2 audits are complete: Vibe reported one MAJOR, two MINORS, and one LOW issue (BLOCKED); Technical Cofounder returned CLEAR. Both raw outputs and prompts are preserved and hash-pinned below; both are advisory only, not the independent review gate.

Official docs (current upstream, supplemental only; not a substitute for local pinned source): [Tool Search](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search), [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills), [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory), [Memory Provider Plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin), [Tools & Toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools), [Curator](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator). Current docs may describe later behavior; local source above governs this host.

## RepoHunt candidates — immutable source snapshots

RepoHunt was discovery, not evaluation/adoption. `git ls-remote` observed the following refs on 2026-10-03:

- **GBrain:** `garrytan/gbrain` `master` → `109b992172e1f49107f9de9841758c1d043a2668`.
  - Pinned raw source: [`skills/RESOLVER.md`](https://raw.githubusercontent.com/garrytan/gbrain/109b992172e1f49107f9de9841758c1d043a2668/skills/RESOLVER.md); snapshot `evidence/upstream/gbrain-RESOLVER-109b992172e1f49107f9de9841758c1d043a2668.md`; SHA-256 `9c55394405c5cf5f477e3f8a0357e6afed8d58562e70ffe35a4f0bddce2ef24f`.
  - Pinned install guide: [`INSTALL_FOR_AGENTS.md`](https://raw.githubusercontent.com/garrytan/gbrain/109b992172e1f49107f9de9841758c1d043a2668/INSTALL_FOR_AGENTS.md); snapshot in `evidence/upstream/`; SHA-256 `357a37a93c4f00ee3fc2ac565a13c7b1df963e7ae489fe94dba54c627e92d3c1`.
  - Pinned license: [`LICENSE`](https://raw.githubusercontent.com/garrytan/gbrain/109b992172e1f49107f9de9841758c1d043a2668/LICENSE); SHA-256 `e56fbb5b3d95756f3fa1cfefa24732ec79f18ece1ad08a4e79e00df57e8b198c`.
  - Disposition: **REFERENCE** explicit trigger→skill resolver only; no install/adoption.
- **Agentmemory:** `rohitg00/agentmemory` `main` → `2a00e7b38fc4ae4e38af4134586be0bbe9612706`.
  - Pinned Hermes integration README: [`integrations/hermes/README.md`](https://raw.githubusercontent.com/rohitg00/agentmemory/2a00e7b38fc4ae4e38af4134586be0bbe9612706/integrations/hermes/README.md); snapshot in `evidence/upstream/`; SHA-256 `464d08e453eba89f22975a5515e701d41cf5af6119c76130ee7274be146945f4`.
  - Pinned license: [`LICENSE`](https://raw.githubusercontent.com/rohitg00/agentmemory/2a00e7b38fc4ae4e38af4134586be0bbe9612706/LICENSE); SHA-256 `76c8d49ab42216a2533f603fbafa20a1bf71b56de136a401be52da034dcc012c`.
  - Disposition: **AVOID as replacement; REFERENCE only**. README describes a separate service, MCP surface, and lifecycle hooks; this is not independent evidence of its benchmark claims.

The files above are exact raw bytes fetched from the pinned commit URLs (not transformed GitHub HTML). The license files are preserved beside the source snapshots.

## Review provenance

- Round 1 result: `evidence/reviews/round-1/REVIEW-RESULT.txt`, SHA-256 `ef4597ad0f1442589475f5d6ed021b125ef70f76edbe78448ef6586e0626739f`; prompt `evidence/reviews/round-1/REVIEW-PROMPT.txt`, SHA-256 `ce1ea48c913142d3c732d8bed7bab52273f7b849ec96f8d0ad2fa4568f8bba52`.
- Round 2 result: `evidence/reviews/round-2/REVIEW-RESULT.txt`, SHA-256 `2f0178e371ddb94ee81e3923bc23259ab9076a79bea5332551f9875f1a2f8045`; prompt `evidence/reviews/round-2/REVIEW-PROMPT.txt`, SHA-256 `8974b685c3f04368b1700add39b2620a048850a1be6faa46f0285235a8cf7246`.
- Round 2 verdict: `NO-GO-WITH-CONDITIONS`; it matched all 11 frozen files before/after inspection and left 5 MAJOR + 1 MINOR + 1 LOW finding. Exact list and dispositions are in `DECISIONS.md`.
- This G0 version changes reviewed plan/control bytes; neither prior verdict authorizes R0. A fresh exact-hash review is required.

## G0 partner-review evidence (advisory; not the independent gate)

- Vibe v2 prompt `evidence/quality/bot-g0-v2-vibe-prompt.txt`, SHA-256 `4c44fe9e3ba4f25cea31fa939cfc7b7057ade526fae0ca91774893ba39b432c5`; raw output `evidence/quality/bot-g0-v2-vibe-review.txt`, SHA-256 `99353188d3bedf267c8db16de521803cf82e27f0c1c11b1c345600c4027bbea3` (4,637 bytes). It returned BLOCKED with one MAJOR (R0b output-channel containment), two MINORS (failure-category/reveal-stage terminology; malformed receipt test cases), and one LOW (README status wording). Each is dispositioned in D-012; no live data was accessed.
- Technical Cofounder v2 prompt `evidence/quality/bot-g0-v2-cofounder-prompt.txt`, SHA-256 `ddfd10cb7288f460ce8a7fb2757803612ba23dca50014c251408a0258fbe69f4`; raw output `evidence/quality/bot-g0-v2-cofounder-review.txt`, SHA-256 `a9520f78ceb36c6a81f02cb98f7dad19ad005fd3e21224bc10c537da73f8d9e8` (967 bytes). It read all 13 assigned files and returned CLEAR; no findings. This does not supersede the round-2 independent NO-GO or authorize R0.

