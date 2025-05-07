import enum

class Model(enum.Enum):
    MISTRAL = "mistral:7b-instruct-v0.3-q3_K_M"
    DEEPSEEK = "deepseek-coder:6.7b-instruct-q3_K_M"
    QWEN = "qwen2.5-coder:3b-instruct-q8_0"
    GEMMA = "gemma3:4b-it-q4_K_M"
    PHI4 = "phi4-mini:3.8b-q4_K_M"
