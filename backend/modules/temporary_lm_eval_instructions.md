## Running the lm_eval_runner Module
This module benchmarks your local or Hugging Face-hosted models using the lm-evaluation-harness on the HumanEval task.
Please read carefully and until the end of the file where I list some known issues.

## How to Run
Run the module as part of the backend pipeline like this:

```python backend/main.py --modules lm_eval_runner```

It will:

Execute the HumanEval test suite

Automatically save the result to 

```outputs/human_eval/```

Print the pass@1 score to the console
 
## Model Selection
You can edit the model that gets evaluated inside LmEvalRunner (modules/lm_eval_runner.py).

### Example: using a CPU-based Hugging Face model

```"--model_args", "pretrained=microsoft/phi-1_5,device=cpu"```

To switch models, change the PATH for pretrained=  to any valid Hugging Face model ID.
You can find model IDs at: https://huggingface.co/models
Right know the model we use for lm_eval is the small one, our bigger 7B models are to much for my cpu.

## CUDA Support
If your machine has a GPU, change:

```device=cpu```
to:
```device=cuda```
for a better performance.

## Tasks & Parameters Used in lm-eval
The evaluation is configured to run the humaneval task, which benchmarks code generation capabilities. It tests whether the model can complete programming functions given partial code and docstrings, using metrics like pass@1.

### Task

```--tasks humaneval```

This runs the HumanEval benchmark from OpenAI — a widely used dataset for evaluating code completion.

You can list all available tasks with:

```lm_eval --tasks list```

There is a variety of different tasks and benchmarks provided in this list, human_eval is the most suitable for us, because is evalutates code generation.
To run a single specific test, you can also limit the run (e.g., --limit 1).

## Parameters Explained
Here’s what each CLI argument passed to lm_eval does:

--model hf:	Use Hugging Face model backend
--model_args:	Passes model config: pretrained=<HF_ID>,device=cpu/cuda
--tasks humaneval:	Run only the HumanEval task
--limit 1:	Limits evaluation to 1 sample (for testing only)
--batch_size 1:	Evaluation batch size
--output_path:	Where to store the output .json file
--confirm_run_unsafe_code:	Required for HumanEval; confirms you understand the code will be executed 🔐

## 🛑 Known Issues

- ️ Large models can freeze or crash if you run them on CPU. Use small models like microsoft/phi-1_5 for testing.

-  The script may hang or silently fail if the model is too large for your system memory.

- If lm_eval is not installed or doesn’t work:

```pip install git+https://github.com/EleutherAI/lm-evaluation-harness.git --force-reinstall```

You must be logged in to Hugging Face:

```huggingface-cli login```

And in some cases, grant access to gated models manually on the model’s page at huggingface.co.

## Output
Results are saved to:

```outputs/human_eval/result_<timestamp>.json```

And a summary is printed to the terminal.

