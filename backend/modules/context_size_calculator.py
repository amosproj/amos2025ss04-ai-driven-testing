from modules.base import ModuleBase
from transformers import AutoTokenizer
from schemas import PromptData
import re
import os
import warnings


class ContextSizeCalculator(ModuleBase):
    def __init__(self):
        self.tokenizer = None
        self.tokenizer_model_id = None

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return False

    def process_prompt(self, prompt_data: PromptData):
        # Get model ID from prompt data
        model_id = prompt_data.model.id

        # Count tokens using the Hugging Face tokenizer
        print(f"[ContextSizeCalculator] Counting tokens for model: {model_id}")

        # Construct full text (user + code + system)
        full_text = (
            prompt_data.input.user_message
            + "\n"
            + prompt_data.input.source_code
            + "\n"
            + prompt_data.input.system_message
        )
        # might be one token off
        token_count = self._count_tokens_with_tokenizer(full_text, model_id)

        # If tokenizer is unavailable, estimate token count
        if token_count is None:
            print(
                "[ContextSizeCalculator] Tokenizer unavailable, estimating token count..."
            )
            token_count = self._estimate_token_count(full_text)
            print(
                f"[ContextSizeCalculator] Estimated token count: {token_count}"
            )
            prompt_data.token_count = token_count
            prompt_data.token_count_estimated = True
        else:
            print(f"[ContextSizeCalculator] Token count: {token_count}")
            prompt_data.token_count = token_count
            prompt_data.token_count_estimated = False

        max_ctx_size = prompt_data.input.options.num_ctx

        # TODO include system prompt etc in calculation when available
        if token_count > max_ctx_size:
            raise ValueError(
                f"Token count ({token_count}) exceeds maximum context size ({max_ctx_size}) by {token_count - max_ctx_size} tokens."
            )

        return prompt_data

    def process_response(self, response_data, prompt_data):
        return response_data

    def _count_tokens_with_tokenizer(self, text, model_id):
        """
        Count tokens using the tokenizer specific to the model
        """
        hf_model_id = self._get_huggingface_model_id(model_id)

        if hf_model_id is None:
            return None

        # Only load the tokenizer if we haven't already loaded it for this model
        if self.tokenizer is None or self.tokenizer_model_id != hf_model_id:
            self.tokenizer = self._load_tokenizer(hf_model_id)
            if self.tokenizer is None:
                return None
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
        local_path = os.path.join(
            os.path.dirname(__file__),
            "context_size_calculator",
            "tokenizers",
            local_model_name,
        )

        # Try loading from local cache first
        if os.path.exists(local_path):
            try:
                print(
                    f"[ContextSizeCalculator] Loading tokenizer from local cache: {local_path}"
                )
                return AutoTokenizer.from_pretrained(local_path)
            except Exception as e:
                warnings.warn(
                    f"[ContextSizeCalculator] Error loading local tokenizer: {e}",
                    UserWarning,
                )
        else:
            print(
                f"[ContextSizeCalculator] Local tokenizer not found at: {local_path}"
            )

        # Fall back to downloading from Hugging Face using download_tokenizer.py
        print(
            "[ContextSizeCalculator] Attempting to download tokenizer using download_tokenizer.py..."
        )
        success = self._download_tokenizer(hf_model_id)
        if success:
            # Try loading the newly downloaded tokenizer
            try:
                print(
                    f"[ContextSizeCalculator] Loading newly downloaded tokenizer from: {local_path}"
                )
                return AutoTokenizer.from_pretrained(local_path)
            except Exception as e:
                warnings.warn(
                    f"[ContextSizeCalculator] Error loading downloaded tokenizer: {e}",
                    UserWarning,
                )

        else:
            warnings.warn(
                f"[ContextSizeCalculator] Failed to download tokenizer for model {hf_model_id}. Consider manually adding it. For further info see: modules/context_size_calculator/README.md",
                UserWarning,
            )
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
            "tinyllama": "TinyLlama/TinyLlama-1.1B-Chat-v0.6",
            "qwen3:4b-q4_K_M": "Qwen/Qwen3-4B",
        }

        # Try exact match first
        if model_id in model_mapping:
            return model_mapping[model_id]

        # Default to a general tokenizer if we can't find a match
        warnings.warn(
            f"No match found for model_id '{model_id}', consider manually adding it. For further info see: modules/context_size_calculator/README.md",
            UserWarning,
        )
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
        word_count = len(re.findall(r"\b\w+\b", text))
        punctuation_count = len(re.findall(r"[.,!?;:]", text))
        word_estimate = word_count + punctuation_count * 0.5

        # Space-based tokenization
        space_estimate = len(text.split())

        # Return the highest estimate to be conservative (as integer)
        return int(max(char_estimate, word_estimate, space_estimate))

    def _download_tokenizer(self, hf_model_id, force=False):
        """Download and save a tokenizer for the given model_id"""

        # Get the tokenizers directory relative to this module
        tokenizers_dir = os.path.join(
            os.path.dirname(__file__), "context_size_calculator", "tokenizers"
        )

        # Create a safe filename for the tokenizer directory
        safe_name = hf_model_id.replace("/", "_")
        tokenizer_dir = os.path.join(tokenizers_dir, safe_name)

        # Check if tokenizer already exists
        if os.path.exists(tokenizer_dir) and not force:
            return True

        # Try to download the tokenizer
        print(
            f"[ContextSizeCalculator] Downloading tokenizer for {hf_model_id}..."
        )
        try:
            tokenizer = AutoTokenizer.from_pretrained(hf_model_id)
            tokenizer.save_pretrained(tokenizer_dir)
            print(
                f"[ContextSizeCalculator] Successfully downloaded and saved tokenizer to {tokenizer_dir}"
            )
            return True
        except Exception as e:
            print(f"[ContextSizeCalculator] attempt failed: {e}")
            return False
