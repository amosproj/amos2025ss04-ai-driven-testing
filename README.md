

# AI-Driven Testing Project
This repository contains the code and tests for the AI-Driven Testing project (AMOS SS 2025).
## 🧠 Project Goal

The goal of this project is to develop or customize a **LLM-based (Large Language Model) AI** that can automatically **generate test code** for existing software. The AI is controlled through a **chat-based interface** and can be provided with information about the target software in various ways.

## 🎯 Main Features (WIP)

- 🔍 **Test Code Generation**  
  The AI can generate test code for arbitrary software using methods such as Retrieval-Augmented Generation (RAG), fine-tuning, or prompting.

- 🔄 **Incremental Test Extension**  
  The AI can recognize and expand existing test code intelligently.

- 🧪 **Understanding of Test Types**  
  The AI can distinguish between different layers and types of tests:
  - **Layers**: User interface, domain/business logic, persistence layer
  - **Test Types**: Unit test, integration test, acceptance test

- 🛠️ **On-Premise Operation**  
  The solution can run fully offline, suitable for on-premise environments.

- 🐳 **Docker Support**  
  The backend can run inside a Docker container and be accessed via an API.

- 🔌 **IDE Integration**  
  The solution can be embedded into existing **open-source development environments**.

## 🚀 Usage Workflow

1. Provide the software (source code or API/documentation)
2. Start the AI and interact through the chat interface
3. Generate and review test code
4. Integrate test code into your existing test suite

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