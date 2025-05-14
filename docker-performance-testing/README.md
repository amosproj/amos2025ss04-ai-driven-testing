# Performance Testing Tool for LLM Models

This directory contains tools for 



performance testing of Large Language Model (LLM) Docker containers. The tools help assess the resource utilization (CPU, memory, GPU) of different models during execution and provide visualizations of the performance metrics.

## Overview

The performance testing framework helps evaluate:

- Resource utilization patterns of LLM containers
- Comparison of different models' resource requirements
- Impact of running multiple models simultaneously vs. sequentially
- Performance overhead of idle containers

## Components

The main components of the performance testing framework are:

- `run_performance_test.py`: The main script for running performance tests
- `performance_monitor.py`: Monitors system and container resource usage
- `performance_visualization.py`: Generates visualizations from test data
- `prompt.txt`: Default prompt file used for testing the models

## Testing Modes

The framework currently supports two testing modes:

1. **sequential**: Start, test, and stop one model at a time
2. **sequential_all_containers**: Start all containers first, then test each sequentially, and stop all at the end

## Usage

### Basic Usage

```bash
# Run using default settings (sequential_all_containers mode with default models)
python run_performance_test.py

# Run in sequential mode (testing one model at a time)
python run_performance_test.py --mode sequential

# Test specific models
python run_performance_test.py --models mistral:7b-instruct-v0.3-q3_K_M phi4-mini:3.8b-q4_K_M

# Use a custom prompt file
python run_performance_test.py --prompt-file custom_prompt.txt

# List available models
python run_performance_test.py --list-models
```

### Command Line Arguments

- `--mode, -m`: Test mode (`sequential` or `sequential_all_containers`)
- `--models`: Space-separated list of model IDs to test
- `--prompt-file, -p`: Path to a file containing the prompt to send
- `--output-dir, -o`: Directory to save test results
- `--list-models`: List available models and exit

## Output and Results

Each test run creates a timestamped directory under `performance_results/` containing:

```
performance_results/
└── run_YYYYMMDD_HHMMSS/
    ├── raw_data/             # Raw performance data in JSON format
    │   ├── sequential_*.json # Performance data files for each model
    │   └── *_report.txt      # Summary reports
    ├── visualizations/       # Generated charts and graphs
    │   ├── system_usage_*.png
    │   ├── gpu_usage_*.png
    │   └── container_*.png
    └── *_summary_*.json      # Summary metadata for the test run
```

## Visualizations

The testing framework generates several visualizations:

- System resource usage (CPU, memory)
- GPU utilization and VRAM usage (if GPUs are available)
- Per-container CPU and memory usage

## Requirements

- Python 3.6+
- Docker
- LLM models available as Docker containers
- GPU (optional, for GPU metrics)

## Setup

The testing framework relies on the `LLMManager` from the backend module for managing LLM containers. Make sure the backend is properly configured before running performance tests.

## Notes

- Performance metrics are collected at 1-second intervals by default
- The framework will automatically create the necessary directories for output
- Containers are started/stopped as needed based on the testing mode
