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

    @classmethod
    def get_model(cls, number: int) -> "Model":
        """Get the model identifier string by its index number.

        Args:
            number: Integer index of the model in the enum (0-based)

        Returns:
            Model: The model object

        Raises:
            ValueError: If the provided number is out of valid range
        """
        models = list(cls)
        if 0 <= number < len(models):
            return models[number]
        raise ValueError(
            f"Invalid model number. Choose between 0-{len(models)-1}"
        )
