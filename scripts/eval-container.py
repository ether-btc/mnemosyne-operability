#!/usr/bin/env python3
"""Evaluate Bekko model on holdout set inside container."""
import json
import sys
from pathlib import Path

# Add model directory to path
sys.path.insert(0, "/app/model")
from inference_v0 import BekkoSentenceTransformer

# Load model
m = BekkoSentenceTransformer('/app/model', device='cpu', trust_remote_code=True)
print('MODEL_LOADED')

# Load holdout
holdout = [json.loads(l) for l in open('/app/model/holdout.jsonl')]
print('HOLDOUT_SIZE:', len(holdout))

# Build requests
reqs = []
for r in holdout:
    reqs.append({
        'state_json': r['query_parts']['context'],
        'decisions': [{
            'id': 'agent_action',
            'kind': 'judgment',
            'type': 'choice',
            'instructions_json': json.dumps(r['query_parts']['instruction']),
            'system_prompt': '',
            'criteria': [{'id': c, 'description_json': json.dumps(c), 'value': None} 
                        for c in r['metadata']['candidate_ids']],
            'documents': [],
            'scoring': None,
        }],
    })

# Predict
res = m.predict(reqs, show_progress_bar=False)
correct = 0
for r, pred in zip(holdout, res):
    probs = pred['agent_action']['probabilities']
    cands = r['metadata']['candidate_ids']
    pick = max(cands, key=lambda c: float(probs.get(c, 0.0)))
    exp = r['_meta']['label']
    ok = pick == exp
    correct += ok
    print(f'  {r["_meta"]["id"]}: pick={pick} exp={exp} {"OK" if ok else "MISS"}')

print(f'ACCURACY: {correct}/{len(holdout)} = {correct/len(holdout):.2f}')
