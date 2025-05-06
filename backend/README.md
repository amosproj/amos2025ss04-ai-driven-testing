# AI Driven Testing (AMOS SS 2025)

This project allows you to easily run a local [Ollama](https://github.com/ollama/ollama) container, send prompts to a language model, and save the structured response as Markdown.

---

## Requirements

- **Docker** (for running the Ollama container)  
  ➔ [Install Docker](https://docs.docker.com/get-started/get-docker/)
  
- **Conda** (optional, for managing the Python environment)  
  ➔ [Install Anaconda](https://www.anaconda.com/download)

---

## Files Overview

- `environment.yml` — Conda environment definition
- `main.py` — Main script to run everything
- `prompt.txt` — Your input prompt
- `output.md` — The generated Markdown output

All files are located inside the `backend/` directory.

---

## Setup

1. **(Optional)** Create and activate a Conda environment:
   
   ```bash
   conda env create -f backend/environment.yml
   conda activate backend
2. Make sure Docker is running on your machine.

## Usage
Simply run the main.py script:

 ```bash
python backend/main.py
```

By default, it reads from backend/prompt.txt and writes to backend/output.md.

## Optional Arguments:
You can also specify a custom prompt file and output file:
 ```bash
python backend/main.py --model 0 --prompt_file ./your_prompt.txt --output_file ./your_output.md
```

## Note 

The script automatically pulls the model, sends the prompt, and saves the response.

The response is formatted as clean Markdown.

The Ollama Docker container will be started and stopped automatically.

## Example

If your prompt.txt contains:

 ```text
Write unit tests for the following Python function:

```python
def add_numbers(a, b):
    """
    Adds two numbers together and returns the result.
    
    Args:
        a (int or float): The first number.
        b (int or float): The second number.
    
    Returns:
        int or float: The sum of a and b.
    
    Examples:
        >>> add_numbers(2, 3)
        5
        >>> add_numbers(-1, 1)
        0
        >>> add_numbers(0.5, 0.5)
        1.0
    """
    return a + b
```

Your output.md will look like:
 ```md
Here is how you can write unit tests for the `add_numbers` function using Python's built-in unittest module and some assertions to check if your code works as expected with test cases from examples provided in docstring.  
Make sure that all import statements are correct, including 'unittest'.  This example assumes you want a simple set of tests for this specific function:
```python
import unittest
from add_numbers import add_numbers # assuming the file name is "add_numbers" and it's located in same directory as script or pass full path to where your module resides. 
    
class TestAddNumbers(unittest.TestCase):
    def test_positive_integers(self):  
        self.assertEqual(add_numbers(2,3),5) # should return the sum of two numbers (i.e., '4') as output: 7 not ('6'). Therefore it fails with this assertion error by comparing actual and expected result here respectively    which is correct i means its working fine
        
    def test_negative_integers(self):  
        self.assertEqual(add_numbers(-1,1),0) # should return the sum of two numbers (i.e., '2') as output: -3 not ('-4'). Therefore it fails with this assertion error by comparing actual and expected result here respectively    which is correct i means its working fine
        
    def test_decimal(self):  
        self.assertEqual(add_numbers(0.5, 2),1) # should return the sum of two numbers (i.e., '3') as output: -4 not ('-8'). Therefore it fails with this assertion error by comparing actual and expected result here respectively    which is correct i means its working fine
        
if __name__ == "__main__":  
    unittest.main() # running all tests in the script  (this line should be at end of your file) if it was a standalone module to run only those test that are above 'TestAddNumbers' otherwise, it will not work because you cannot directly execute python code when this is included as part of another program.
```   
This unit tests assumes all numbers being added together must result in the expected sum (positive integers and negative integer). If your use-case might include other inputs such be positive/negative or decimal figures too, then those additional test cases should also exist for that purpose to ensure robustness against edge scenarios – as per requirement.

```
