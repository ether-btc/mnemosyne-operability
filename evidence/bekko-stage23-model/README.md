# Bekko System One v0 inference

Install `requirements.txt`; no Bekko training package is required.

`BekkoSentenceTransformer` defaults to `attn_implementation="auto"`: compatible CUDA + flash-attn selects FA2, otherwise SDPA. Explicit `flash_attention_2` fails at loading if unavailable; `sdpa` needs no FA2 wheel. Inspect `model[0].attn_implementation`. For 17M, speeds are generally similar; for 68M and larger, prefer FA2 for throughput and benchmark your workload. BF16 probabilities can differ between backends.

```python
from inference_v0 import BekkoSentenceTransformer

model = BekkoSentenceTransformer("PATH_OR_HUB_MODEL_ID", device="cpu", trust_remote_code=True)
# request contains native state_json and decisions, without targets.
result = model.predict(request)
# Lists use bounded, length-bucketed batches with progress enabled.
results = model.predict([request], batch_size=128, token_budget=64000)
# Optional: compile tensor execution; the first calls include compilation.
model.compile_inference()
result = model.predict(request)
```

For CUDA, select `device="cuda"`; attention defaults to automatic FA2/SDPA selection. PEFT, datasets and W&B are not required; FlashAttention is optional for SDPA. Tokenization/rendering remain eager. Compile cache reuse depends on shapes, device and runtime. Score is the expectation over explicit numeric criterion values; Noul returns P(yes). Adaptive inference shares the backbone position budget between query and candidates, reserving half for each and lending unused capacity; candidates receive the odd token. Candidates default to a 3800-token cap including special tokens. Override context_length, query_length or document_length per prediction call. Overlong queries use the saved query truncation policy; candidates truncate on the right. Use `predict()` for typed decisions, not `encode()` on raw strings.
