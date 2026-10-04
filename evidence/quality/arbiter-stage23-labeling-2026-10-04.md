Receipt trail complete (pre-registered call → consult attempt → UNAVAILABLE degradation, all appended). Jev contributed nothing (401), so per the fail-closed rule I decide solo. My pre-registered call stands.

---

**VERDICT: PROCEED-AMENDED — Option C now (hand-label Stage 2/3). Option A demoted from "alternative" to "parallel prep task." Do not fine-tune yet.**

**Reasoning:**

1. **The blocker is a model-capability floor, not a prompt problem.** Six independent elicitation strategies — including few-shot with explicit examples and a radical output-format change (A/B/C/D letters) — all returned the Stage 1 JSON. Nothing prompt-shaped survives that; option B (decider-0.8b) is a *smaller* model of the same class and is dominated.

2. **LoRA on this corpus is circular and unfalsifiable.** Stage 2/3 applies to at most the 33 eligible task-starts. Fine-tuning on ~30 examples gives you a labeler with no held-out set, trained on the very labels the study is trying to measure. That's weaker evidence than a careful human rater, not stronger — it fails your own validity criterion.

3. **A is blocked on an external dependency with unknown ETA; C is not.** Stage 2/3 gates the entire study. Hand-labeling ~33 items with a written codebook is hours, not days. Waiting for an SSH restart stalls a completable stage for no validity gain.

4. **The study is valid without model-based Stage 2/3.** Single-rater manual labeling is standard at this n; the honest threat is rater bias, which you mitigate procedurally (see amendment), not by swapping in an overfit 1.5b model.

5. **A and C are complementary, not competing — which is exactly why "wait for A" is strictly dominated.** Your hand labels become the training/validation set if automation is ever needed later. The technical-cofounder's ladder is correct in shape but exhausted through its second rung; LoRA remains the documented backup with a defined trigger (below).

**Amendment (do now):**
- Write a short codebook operationalizing "avoidable reminder" *before* labeling; label all eligible task-starts with it.
- Re-rate a random 20% sample after ≥48h; report intra-rater agreement in the study writeup.
- In parallel, request the a16 SSH restart (zero marginal cost) — but nothing blocks on it.
- LoRA trigger condition (all three): a16 reachable AND future batches need the labeling automated AND the model is validated against your hand labels as an independent second rater. That reframes A from rescue plan to validation instrument.

**Assumptions:** (i) Stage 2/3 labeling scope ≈ 33 items — if it's 100+, the time cost changes but C still wins; (ii) you are a competent rater for this construct (your claim, unverified by me — the codebook + re-rating sample is the mitigation); (iii) no second human rater is available — if one is, add inter-rater agreement on a 20% sample and validity strengthens further.

**Invalidation:** If Stage 2/3 turns out to be a deterministic transform of Stage 1 data (no judgment required), no labeling is needed at all — write the transform. Conversely, if hand-labeling reveals you cannot operationalize "avoidable reminder" reproducibly, that is a construct-validity problem no labeling route fixes — bring it back as a new fork.

*Consult note: Jev advisory UNAVAILABLE (HTTP 401 ×2), receipted as degraded; decision made solo per ADR-021 fail-closed rule. Decision ID: arb-20261004-stage23-labeling.*
