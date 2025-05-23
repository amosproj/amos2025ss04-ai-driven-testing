#!/usr/bin/env python3
"""
Test script for context size calculator tokenizers
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from context_size_calculator import ContextSizeCalculator

def test_tokenizers():
    """Test all available tokenizers with sample texts"""
    
    # Test models from allowed_models.json
    test_models = [
        "mistral:7b-instruct-v0.3-q3_K_M",
        "deepseek-coder:6.7b-instruct-q3_K_M", 
        "qwen2.5-coder:3b-instruct-q8_0",
        "gemma3:4b-it-q4_K_M",
        "phi4-mini:3.8b-q4_K_M",
        "tinyllama"
    ]
    
    # Test texts of varying sizes
    test_texts = {
        "small": "Hello, how are you today?",
        "medium": """
        This is a medium-sized text that contains multiple sentences.
        It includes some technical content about programming and AI models.
        The purpose is to test tokenization accuracy across different model tokenizers.
        We want to ensure that our context size calculator works correctly.
        """.strip(),
        "large": """
        This is a larger text sample that will help us test the tokenization capabilities
        of different models. The text contains various elements including:
        
        1. Programming concepts like variables, functions, and algorithms
        2. Natural language processing terminology
        3. Mathematical symbols and expressions: x = y + z, f(x) = 2x + 1
        4. Code snippets: 
           def hello_world():
               print("Hello, World!")
               return True
        
        5. Special characters and punctuation: !@#$%^&*()_+-={}[]|\\:";'<>?,.
        
        The goal is to ensure that our tokenizer can handle diverse content types
        and provide accurate token counts that will help with context window management.
        This includes handling edge cases like code blocks, mathematical notation,
        and various forms of punctuation that might appear in real-world usage.
        
        Additionally, we want to test how different tokenizers handle the same content,
        as each model may have its own specific tokenization strategy and vocabulary.
        """.strip()
    }
    
    calculator = ContextSizeCalculator()
    
    print("=" * 80)
    print("CONTEXT SIZE CALCULATOR - TOKENIZER TEST")
    print("=" * 80)
    
    results = {}
    
    for model_id in test_models:
        print(f"\n🔍 Testing model: {model_id}")
        print("-" * 50)
        
        results[model_id] = {}
        
        for text_name, text in test_texts.items():
            try:
                token_count = calculator._count_tokens_with_hf(text, model_id)
                results[model_id][text_name] = token_count
                print(f"  {text_name:8} text: {token_count:4d} tokens")
            except Exception as e:
                print(f"  {text_name:8} text: ERROR - {e}")
                results[model_id][text_name] = f"ERROR: {e}"
    
    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY - TOKEN COUNTS BY MODEL")
    print("=" * 80)
    print(f"{'Model':<35} {'Small':<8} {'Medium':<8} {'Large':<8}")
    print("-" * 80)
    
    for model_id, counts in results.items():
        small = counts.get('small', 'N/A')
        medium = counts.get('medium', 'N/A')
        large = counts.get('large', 'N/A')
        
        # Format numbers nicely, handle errors
        small_str = f"{small}" if isinstance(small, int) else "ERROR"
        medium_str = f"{medium}" if isinstance(medium, int) else "ERROR"
        large_str = f"{large}" if isinstance(large, int) else "ERROR"
        
        print(f"{model_id:<35} {small_str:<8} {medium_str:<8} {large_str:<8}")
    
    # Test tokenizer availability
    print("\n" + "=" * 80)
    print("TOKENIZER AVAILABILITY")
    print("=" * 80)
    
    tokenizers_dir = os.path.join(os.path.dirname(__file__), "tokenizers")
    if os.path.exists(tokenizers_dir):
        available_tokenizers = os.listdir(tokenizers_dir)
        print(f"Available local tokenizers: {len(available_tokenizers)}")
        for tokenizer in sorted(available_tokenizers):
            print(f"  ✅ {tokenizer}")
    else:
        print("❌ No local tokenizers directory found")
    
    print(f"\nTotal models tested: {len(test_models)}")
    successful_tests = sum(1 for model, counts in results.items() 
                          if all(isinstance(count, int) for count in counts.values()))
    print(f"Successful tokenizations: {successful_tests}/{len(test_models)}")
    
    return results

if __name__ == "__main__":
    test_tokenizers()
