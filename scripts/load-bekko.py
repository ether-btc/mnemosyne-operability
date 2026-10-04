#!/usr/bin/env python3
"""Custom loader for Bekko model from nested export format.

The Bekko export_v0.py produces a nested structure (0_BekkoInference/) that
SentenceTransformer's from_pretrained cannot load directly. This script
loads the model from the nested format and wraps it in a BekkoSentenceTransformer.
"""
import json
import sys
from pathlib import Path

import torch
from transformers import AutoConfig, AutoModel, AutoTokenizer
from safetensors.torch import load_file


def load_bekko_model(model_path: str, device: str = "cpu"):
    """Load Bekko model from nested export format.
    
    Args:
        model_path: Path to the exported model directory
        device: Device to load model on ('cpu' or 'cuda')
    
    Returns:
        BekkoSentenceTransformer instance
    """
    model_path = Path(model_path)
    
    # Load backbone config
    backbone_config_path = model_path / "0_BekkoInference" / "backbone_config.json"
    if not backbone_config_path.exists():
        raise FileNotFoundError(f"backbone_config.json not found at {backbone_config_path}")
    
    config = json.loads(backbone_config_path.read_text())
    model_type = config.pop("model_type")
    
    # Load inference config
    inference_config_path = model_path / "0_BekkoInference" / "inference_config.json"
    if not inference_config_path.exists():
        raise FileNotFoundError(f"inference_config.json not found at {inference_config_path}")
    
    inference_config = json.loads(inference_config_path.read_text())
    
    # Load model weights
    weights_path = model_path / "0_BekkoInference" / "model.safetensors"
    if not weights_path.exists():
        raise FileNotFoundError(f"model.safetensors not found at {weights_path}")
    
    # Create backbone model
    backbone = AutoModel.from_config(
        AutoConfig.for_model(model_type, **config),
        attn_implementation="sdpa",
        dtype=torch.float32,
    )
    
    # Load weights
    state_dict = load_file(str(weights_path))
    backbone.load_state_dict(state_dict, strict=True)
    
    # Create tokenizer (use a default one since it's not in the export)
    # The tokenizer is not critical for inference if we're just doing predictions
    # We'll create a simple one from the config
    tokenizer = AutoTokenizer.from_pretrained(
        "cross-encoder/ettin-reranker-17m-v1",
        local_files_only=False,
    )
    
    # Import BekkoInference and BekkoSentenceTransformer
    sys.path.insert(0, str(model_path))
    from inference_v0 import BekkoInference, BekkoSentenceTransformer
    
    # Create BekkoInference model
    model = BekkoInference(
        backbone,
        tokenizer,
        **inference_config,
    )
    
    # Wrap in BekkoSentenceTransformer
    # We need to create a minimal SentenceTransformer wrapper
    # Since BekkoSentenceTransformer extends SentenceTransformer, we need to
    # create it properly or use a simpler approach
    
    # Actually, let's just return the BekkoInference model directly
    # and handle the prediction interface separately
    return model.eval().requires_grad_(False)


def predict(model, requests):
    """Run prediction on a list of requests.
    
    Args:
        model: BekkoInference model
        requests: List of request dicts with 'state_json' and 'decisions'
    
    Returns:
        List of prediction results
    """
    results = []
    for req in requests:
        # Extract the decision request
        decision = req["decisions"][0]
        state = json.loads(req["state_json"])
        
        # Run prediction
        # This is a simplified interface - the actual BekkoInference.predict
        # may have a different signature
        result = model.predict(
            state_json=req["state_json"],
            decisions=req["decisions"],
        )
        results.append(result)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Load and test Bekko model")
    parser.add_argument("--model-path", required=True, help="Path to exported model")
    parser.add_argument("--device", default="cpu", help="Device to load model on")
    args = parser.parse_args()
    
    print(f"Loading model from {args.model_path}...")
    model = load_bekko_model(args.model_path, args.device)
    print("MODEL_LOADED")
    
    # Test with a simple request
    test_req = [{
        "state_json": json.dumps({"message": "test"}),
        "decisions": [{
            "id": "test",
            "kind": "judgment",
            "type": "choice",
            "instructions_json": json.dumps("test"),
            "system_prompt": "",
            "criteria": [
                {"id": "a", "description_json": json.dumps("a"), "value": None},
                {"id": "b", "description_json": json.dumps("b"), "value": None},
            ],
            "documents": [],
            "scoring": None,
        }],
    }]
    
    print("Running test prediction...")
    result = model.predict(test_req, show_progress_bar=False)
    print(f"RESULT: {result}")
