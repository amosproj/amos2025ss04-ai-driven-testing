import enum


class Model(enum.Enum):
    """
    Enumeration of available language models with their Ollama identifiers.

    Each enum value represents a specific model available through Ollama,
    including its version, quantization parameters, and approximate size.
    """

    MISTRAL = "mistral:7b-instruct-v0.3-q3_K_M"  # 3.52 GB
    DEEPSEEK = "deepseek-coder:6.7b-instruct-q3_K_M"  # 3.30 GB
    QWEN = "qwen2.5-coder:3b-instruct-q8_0"  # 3.29 GB
    GEMMA = "gemma3:4b-it-q4_K_M"  # 3.34 GB
    PHI4 = "phi4-mini:3.8b-q4_K_M"  # 2.49 GB
