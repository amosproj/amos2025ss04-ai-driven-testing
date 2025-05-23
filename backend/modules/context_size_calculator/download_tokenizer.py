#!/usr/bin/env python3
"""
Tokenizer Downloader for Context Size Calculator

This script downloads and saves tokenizers for all models defined in allowed_models.json.
The tokenizers are saved to the ./tokenizers directory for offline use.

Usage:
    python download_tokenizers.py              # Download all tokenizers
    python download_tokenizers.py <model_id>   # Download a specific tokenizer
"""

import os
import sys
import json
import argparse
from transformers import AutoTokenizer

# Get the absolute path to the backend directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.dirname(SCRIPT_DIR)
BACKEND_DIR = os.path.dirname(MODULES_DIR)
TOKENIZERS_DIR = os.path.join(SCRIPT_DIR, "tokenizers")

# Ensure tokenizers directory exists
if not os.path.exists(TOKENIZERS_DIR):
    os.makedirs(TOKENIZERS_DIR, exist_ok=True)
    print(f"Created tokenizers directory: {TOKENIZERS_DIR}")

def download_tokenizer(hf_model_id, force=False):
    """Download and save a tokenizer for the given model_id"""
    
    # Create a safe filename for the tokenizer directory
    safe_name = hf_model_id.replace("/", "_")
    tokenizer_dir = os.path.join(TOKENIZERS_DIR, safe_name)
    
    # Check if tokenizer already exists
    if os.path.exists(tokenizer_dir) and not force:
        return True
    
    # Try to download the tokenizer
    print(f"Downloading tokenizer for {hf_model_id}...")
    try:
        # First try without trust_remote_code
        tokenizer = AutoTokenizer.from_pretrained(hf_model_id)
        tokenizer.save_pretrained(tokenizer_dir)
        print(f"Successfully downloaded and saved tokenizer to {tokenizer_dir}")
        return True
    except Exception as e:
        print(f"First attempt failed: {e}")
        print(f"Failed to download tokenizer: {e2}")
        return False
    
def main():
    models = {
            "mistralai/Mistral-7B-Instruct-v0.3",
            "deepseek-ai/deepseek-coder-6.7b-instruct",
            "Qwen/Qwen2.5-Coder-3B-Instruct",
            "google/gemma-3-4b-it",
            "microsoft/Phi-4-mini-instruct",
            "TinyLlama/TinyLlama-1.1B-Chat-v0.6"
        }
    
    for model in models:
        print(f"Downloading tokenizer for {model}...")
        success = download_tokenizer(model)
        if not success:
            print(f"Failed to download tokenizer for {model}")
    
if __name__ == "__main__":
    main()
        


