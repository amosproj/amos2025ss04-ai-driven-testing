.PHONY: format check-format lint test install-dev install-hooks

# Install development dependencies
install-dev:
	pip3 install -r requirements-dev.txt

# Install pre-commit hooks
install-hooks:
	pre-commit install

# Format code with Black
format:
	python3 -m black .

# Check code formatting without making changes
check-format:
	python3 -m black --check --diff .

# Run linting
lint:
	python3 -m flake8 .

# Run tests
test:
	python3 -m pytest

# Run all quality checks
check: check-format lint test

# Setup development environment
setup: install-dev install-hooks
	@echo "Development environment setup complete!"
	@echo "Run 'make check' to verify everything is working."
