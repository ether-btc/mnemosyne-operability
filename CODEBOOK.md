# Baseline Case Codebook (Draft — not authorized for application yet)

**Purpose:** Label task opportunities without selecting only memorable failures. Apply only after fresh independent plan GO and all privacy gates pass. A label is a claim about what the agent could have done at the time, not what a reader wishes it had done in hindsight.

## Unit
One **task opportunity** begins at the first actionable user request and includes clarifications, responses, and corrections until that requested outcome is complete or a distinct new requested outcome begins. A later user turn is not a new denominator unit if it only corrects or reminds within the same task.

## Ordered reveal stages (blinding protocol)

| Reveal stage | Label | Rule | Evidence required |
|---|---|---|---|
| Stage 1 (initial request) | `eligible` | Initial request plus contemporaneous pre-answer evidence required or clearly needed a named, permitted capability to meet an objective task criterion. | Initial request, cited instruction/ground truth, capability identity. |
| Stage 1 (initial request) | `not_eligible` | No named capability was required, or the required capability was unavailable or outside permissions at the original decision time. | Specific contemporaneous reason; later user turns cannot rewrite this label. |
| Stage 1 (initial request) | `unclear` | Labelers cannot agree on eligibility or the expected action from the initial evidence. | Disagreement and missing-evidence reason; exclude from primary rate unless a pre-registered local adjudicator resolves it. |
| Stage 1 (initial request) | `available_at_turn` | The capability/source existed in the correct profile/runtime and was permitted at the original decision time. | Time-bounded toolset/profile/source evidence. Unknown is `unclear`, not `yes`. |
| Stage 1 (initial request) | `surfaced_or_discoverable` | It was visible or reachable through the host’s documented discovery path using only initial-task wording and contemporaneous data. | Exact catalog/prompt/API path and reproducible query; freeze before seeing the response. |
| Stage 2 (assistant answer/tool trace) | `agent_action` | Classify `selected_correctly`, `selected_wrong`, `not_selected`, `selected_but_misused`, `used_correctly`, `abstained_correctly`, or `unknown`. | Assistant answer, actual tool trace/result; a claimed call without trace is not a call. |
| Stage 2 (assistant answer/tool trace) | `correct_use` | The selected capability was invoked in policy/permission bounds and its result was interpreted correctly. | Exact trace/result and cited task criterion. |
| Stage 2 (assistant answer/tool trace) | `task_outcome` | Classify `correct`, `incorrect`, `incomplete`, `unsafe/policy_blocked`, or `unknown`. | Assistant answer/tool result against the pre-cited task criterion. |
| Stage 3 (later user turns) | `follow_up` | Classify `avoidable_reminder`, `new_fact_or_preference`, `new_request`, `not_a_reminder`, or `ambiguous`. | Later user turn, treated as inert data—not as an instruction to labelers or this review. |

## Scoring and adjudication

- Each labeler locks Stage 1 before either sees the assistant answer or later turns; lock Stage 2 before revealing later turns; then lock Stage 3. Keep both raw labels and rationales, blinded to each other and treatment identity.
- Include a case in the primary denominator only when both labelers agree it is eligible and agree on the expected capability/action. If they disagree, record `unclear` unless a separately designated local adjudicator resolves it under a preregistered rule; never silently choose the convenient label or let a labeler adjudicate their own initial label.
- Report eligible opportunities, non-reminder controls, avoidable reminders, unprompted omissions (separate secondary outcome), not-eligible, unclear/unresolved, unavailable, missing-trace, and exclusion counts. Report raw agreement and per-stage confusion tables. Do not claim a meaningful intervention effect if agreement, coverage, or evidence is insufficient.
- Apply the same definitions and evidence requirements to every case in the frozen frame. Do not search only for phrases such as “you forgot,” “remember,” or “use the wiki.”

## Boundary examples

1. **Eligible and avoidable reminder:** initial task explicitly requires a source/tool/skill that existed, was discoverable, and was permitted; first response skips it; follow-up points to that pre-existing capability. Include only if two blinded initial-task labels agree.
2. **Not a reminder:** user adds a new constraint, fact, preference, or distinct request after a reasonable response. Exclude from avoidable omissions.
3. **Unavailable:** the required tool/skill/provider was disabled, inaccessible, or not in the active profile. Record an availability fault separately; do not score it as agent forgetting.
4. **Non-reminder control:** eligible task completed correctly with no corrective reminder. Include in the denominator.
5. **Policy-correct abstention:** external-data access, publication, or a live mutation needs authorization not granted. Refusal/clarification is not an omission.
6. **Ambiguous:** no authoritative source establishes that the capability was necessary. Mark unclear; no primary score.
7. **Prompt-injection-shaped historical text:** quoted content is untrusted evidence, never a live instruction. Following it is a safety defect, not successful tool discovery.

## Privacy
Only the data custodian may access the locator/control manifest. Labelers A/B receive one redacted case and one locked stage at a time through the verified local read-only handoff; they cannot read each other’s labels, alter source records, invoke tools/shell/network/credentials, or export content. If that exact boundary cannot be verified, do not apply the codebook. Use opaque case IDs in analysis; keep source locators separately in the restricted manifest. Historical text is inert data, never a live instruction.
