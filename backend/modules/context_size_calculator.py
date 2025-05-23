from base import ModuleBase
from transformers import AutoTokenizer
import re
import requests
import time
import os

class ContextSizeCalculator(ModuleBase):
    def __init__(self):
        self.tokenizer = None
        self.tokenizer_model_id = None
        self.max_context_size = None
        
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True
    
    def process_prompt(self, prompt_data):
        return prompt_data
    
    def process_response(self, response_data, prompt_data):
        return response_data
    
    def _count_tokens_with_hf(self, text, model_id):
        """
        Count tokens using the Hugging Face tokenizer specific to the model
        """
        hf_model_id = self._get_huggingface_model_id(model_id)
        
        if hf_model_id is None:
            print(f"[ContextSizeCalculator] No tokenizer mapping found for {model_id}")
            return self._estimate_token_count(text)
        
        # Only load the tokenizer if we haven't already loaded it for this model
        if self.tokenizer is None or self.tokenizer_model_id != hf_model_id:
            self.tokenizer = self._load_tokenizer(hf_model_id)
            if self.tokenizer is None:
                print(f"[ContextSizeCalculator] Failed to load tokenizer for {hf_model_id}, falling back to estimation")
                return self._estimate_token_count(text)
            self.tokenizer_model_id = hf_model_id
                
        # Count tokens using the model's tokenizer
        tokens = self.tokenizer.encode(text)
        return len(tokens)
    
    def _load_tokenizer(self, hf_model_id):
        """
        Load tokenizer, trying local cache first, then remote download
        """
        # Convert model ID to directory name (replace / with _)
        local_model_name = hf_model_id.replace("/", "_")
        local_path = os.path.join(os.path.dirname(__file__), "context_size_calculator", "tokenizers", local_model_name)
        
        # Try loading from local cache first
        if os.path.exists(local_path):
            try:
                print(f"[ContextSizeCalculator] Loading tokenizer from local cache: {local_path}")
                return AutoTokenizer.from_pretrained(local_path)
            except Exception as e:
                print(f"[ContextSizeCalculator] Error loading local tokenizer: {e}")
        
        # Fall back to downloading from Hugging Face
        try:
            print(f"[ContextSizeCalculator] Downloading tokenizer for {hf_model_id}...")
            return AutoTokenizer.from_pretrained(hf_model_id)
        except Exception as e:
            print(f"[ContextSizeCalculator] Error downloading tokenizer: {e}")
            return None
        
    def _get_huggingface_model_id(self, model_id):
        """
        Map Ollama model ID to corresponding Hugging Face model ID
        """
        model_mapping = {
            "mistral:7b-instruct-v0.3-q3_K_M": "mistralai/Mistral-7B-Instruct-v0.3",
            "deepseek-coder:6.7b-instruct-q3_K_M": "deepseek-ai/deepseek-coder-6.7b-instruct",
            "qwen2.5-coder:3b-instruct-q8_0": "Qwen/Qwen2.5-Coder-3B-Instruct",
            "gemma3:4b-it-q4_K_M": "google/gemma-3-4b-it",
            "phi4-mini:3.8b-q4_K_M": "microsoft/Phi-4-mini-instruct",
            "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v0.6"
        }
        
        # Try exact match first
        if model_id in model_mapping:
            return model_mapping[model_id]

        # Default to a general tokenizer if we can't find a match
        print(f"[ContextSizeCalculator] No specific tokenizer found for {model_id}, using default tokenizer")
        return None
    
    def _estimate_token_count(self, text):
        """
        Estimate token count for a given text if tokenizer is unavailable.
        This is a rough approximation - actual tokenization varies by model.
        """
        # Simple character-based heuristic (roughly 4 chars per token for English)
        char_count = len(text)
        char_estimate = char_count / 4
        
        # Word-based tokenization (closer to GPT-2/GPT-3 tokenization)
        word_count = len(re.findall(r'\b\w+\b', text))
        punctuation_count = len(re.findall(r'[.,!?;:]', text))
        word_estimate = word_count + punctuation_count * 0.5
        
        # Space-based tokenization
        space_estimate = len(text.split())
        
        # Return the highest estimate to be conservative (as integer)
        return int(max(char_estimate, word_estimate, space_estimate))


