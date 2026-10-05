#!/bin/bash
# Test model locally before containerizing.
# Usage: test-local.sh <model-path>

set -uo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <model-path>"
    exit 1
fi

MODEL_PATH="$1"

echo "=== Testing model locally ==="
echo "Model: $MODEL_PATH"
echo ""

# Check if model files exist
if [ ! -d "$MODEL_PATH" ]; then
    echo "ERROR: Model directory not found: $MODEL_PATH"
    exit 1
fi

# Check for required files
REQUIRED_FILES=("config.json" "model.safetensors")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$MODEL_PATH/$file" ]; then
        echo "WARNING: Missing required file: $file"
    fi
done

# Test loading the model
echo "Testing model load..."
python3 -c "
import sys
sys.path.insert(0, '$MODEL_PATH')
try:
    from inference_v0 import BekkoSentenceTransformer
    m = BekkoSentenceTransformer('$MODEL_PATH', device='cpu', trust_remote_code=True)
    print('MODEL_LOADED')
    
    # Test prediction
    test_req = [{
        'state_json': '{\"message\": \"test\"}',
        'decisions': [{
            'id': 'test',
            'kind': 'judgment',
            'type': 'choice',
            'instructions_json': '\"test\"',
            'system_prompt': '',
            'criteria': [
                {'id': 'a', 'description_json': '\"a\"', 'value': None},
                {'id': 'b', 'description_json': '\"b\"', 'value': None}
            ],
            'documents': [],
            'scoring': None,
        }],
    }]
    result = m.predict(test_req, show_progress_bar=False)
    print('PREDICTION_OK')
    print('Result:', result[0]['test']['probabilities'])
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "=== Local test passed ==="
    echo "Safe to containerize."
    exit 0
else
    echo ""
    echo "=== Local test failed ==="
    echo "Fix issues before containerizing."
    exit 1
fi
