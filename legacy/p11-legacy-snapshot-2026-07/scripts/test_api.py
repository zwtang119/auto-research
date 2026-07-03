#!/usr/bin/env python3
"""Test API connection for P1.1 experiment."""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from inner_monologue_experiment import load_config, call_model

def test_api():
    """Test API connection with a simple prompt."""
    config_path = Path(__file__).parent.parent.parent.parent / "policysim-research-Tsinghua" / "config" / "experiment-config.yaml"
    
    # Load config
    config = load_config(str(config_path))
    
    # Test with deepseek-v4-pro
    model_name = "deepseek-v4-pro"
    
    # Check if API key is available
    model_cfg = config["models"][model_name]
    provider = model_cfg["provider"]
    api_key_env = config["api_endpoints"][provider]["api_key_env"]
    
    print(f"Model: {model_name}")
    print(f"Provider: {provider}")
    print(f"API key env: {api_key_env}")
    print(f"API key set: {bool(os.environ.get(api_key_env))}")
    
    # Try to call the model
    try:
        messages = [{"role": "user", "content": "Hello, please respond with 'OK' to confirm the API is working."}]
        response, usage = call_model(config, model_name, messages, max_tokens=10)
        print(f"Response: {response}")
        print(f"Usage: {usage}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
