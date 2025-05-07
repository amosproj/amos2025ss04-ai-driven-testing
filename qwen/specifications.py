# Edit these specifications to make the model run on your computer
# Give the amos2025ss04-ai-driven-testing file location
from pathlib import Path

# get amos repo
yourAmosDirectory = Path(__file__).resolve().parents[1]

# create path
script_directory = yourAmosDirectory / "qwen"

# Often used values
model_name = "qwen_tester"

code_path = "code_to_test.py"
