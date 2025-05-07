# Fabulous Project (AMOS SS 2025)
if you can read this you don't need glasses - Spaceballs   
If you water an apple tree with apple juice, is that cannibalism?

# AI-Driven Testing Project

This repository contains the code and tests for the AI-Driven Testing project (AMOS SS 2025).

## Project Structure

```
ai-driven-testing/
├── src/
│   └── main/
│       ├── __init__.py
│       └── hello_world.py
└── tests/
    └── test_hello_world.py
```

## Setup Instructions

### Prerequisites

- Python 3.10 or newer
- pip (Python package manager)

### Setting Up the Environment

1. **Create a virtual environment**:

   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Code Quality and Formatting

This project uses Black for code formatting. To ensure your code meets the project's formatting standards:

```bash
# Verify formatting
black --check .

# If issues are reported, fix them automatically with
black .
```

## Running Tests

Execute the tests from the project root directory:

```bash
# Run all tests
pytest

# Run tests with less output
pytest -q

# Run tests with verbose output
pytest -v
```

## Continuous Integration

This project uses GitHub Actions for CI. Each push and pull request triggers:
- Code formatting check with Black
- Linting with Flake8
- Automated tests with Pytest

## Development

When contributing to this project:
1. Create a new branch for your feature/fix
2. Make sure all tests pass locally before pushing
3. Follow the code style guidelines enforced by Black and Flake8

## License

[Look up the file LICENSE]