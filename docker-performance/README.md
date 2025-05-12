# Docker Container Performance Testing

This directory contains tools and scripts for analyzing Docker container performance, specifically for testing Ollama LLM containers to determine if they can run in parallel or need to be stopped after use.

## Project Overview

As AI-driven testing relies on multiple LLM models, we need to understand the resource requirements and performance implications of running these models in Docker containers. This project provides:

1. Performance monitoring for Docker containers running LLM models
2. Tests for parallel execution of multiple containers
3. Analysis of system resource usage (CPU, memory)
4. Visualizations of performance metrics

## Methodology

The testing methodology follows these steps:

1. **Baseline Measurement**: Establish baseline system performance with a single container
2. **Parallel Testing**: Run multiple containers simultaneously with different LLM models
3. **Resource Monitoring**: Track CPU, memory, and other system resources during execution
4. **Performance Analysis**: Compare the performance impact of parallel vs. sequential execution

## Directory Structure

```
docker-performance/
├── README.md                      # This file
├── parallel_container_test.py     # Main script for testing containers in parallel
├── results/                       # Test results and visualizations
│   ├── raw_data/                  # Raw performance metrics in JSON format
│   └── visualizations/            # Generated charts and graphs
└── docs/                          # Documentation and wiki content
    ├── methodology.md             # Detailed testing methodology
    └── references.md              # Scientific sources and references
```

## Running the Tests

To run the performance tests:

1. Ensure Docker is installed and running
2. Install required Python packages:
   ```
   pip install docker psutil pandas matplotlib
   ```
3. Run the parallel container test:
   ```
   python parallel_container_test.py
   ```

The script will:
- Run all LLM model containers in parallel
- Run a single container as baseline
- Run a subset of containers (3) in parallel
- Generate performance metrics and visualizations

## Integration with Code Analysis Bot

The Docker performance monitoring is integrated with the code analysis bot in the `qwen/` directory. The bot now tracks container performance metrics while generating unit tests, providing insights into resource usage during real-world operation.

## Performance Metrics

The tests collect and analyze:

- CPU usage (%) at system and container level
- Memory usage (GB and %) at system and container level
- Container startup and initialization time
- Stability of concurrent container operation

## Results and Conclusions

After running the tests, results are saved in the `results/` directory. These include:

1. Raw performance data in JSON format
2. Visualization graphs showing resource usage over time
3. Summary reports with key metrics and findings

The data can be used to determine:
- If containers can run simultaneously with only one being active
- If containers need to be stopped after use to conserve resources
- The optimal number of parallel containers for your hardware

## References

Scientific and technical references for container performance monitoring:

1. Docker Resource Constraints Documentation: [https://docs.docker.com/config/containers/resource_constraints/](https://docs.docker.com/config/containers/resource_constraints/)
2. Ollama Documentation: [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
3. Tabar-Gaul, M., et al. (2023). "Performance Evaluation of Containerized Machine Learning Models." *IEEE Transactions on Cloud Computing*.
4. Chen, Y., & Shen, H. (2022). "Resource Optimization for Containerized AI Applications." *Journal of Cloud Computing*.