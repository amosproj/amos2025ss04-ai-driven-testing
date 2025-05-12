#!/usr/bin/env python3
"""
Parallel Docker Container Performance Test

This script runs multiple Ollama containers in parallel with different models
and measures their performance impact on the system. It tracks CPU, memory,
and other resource usage metrics to determine if containers can run concurrently
or need to be stopped after use.
"""

import time
import json
import os
import threading
import docker
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from performance_monitor import PerformanceMonitor

# Ensure results directory exists
RESULTS_DIR = Path(__file__).parent / "performance_results"
RESULTS_DIR.mkdir(exist_ok=True)
(RESULTS_DIR / "raw_data").mkdir(exist_ok=True)
(RESULTS_DIR / "visualizations").mkdir(exist_ok=True)

# Define models to test
MODELS = [
    "mistral:7b-instruct-v0.3-q3_K_M",
    "deepseek-coder:6.7b-instruct-q3_K_M",
    "qwen2.5-coder:3b-instruct-q8_0",
    "gemma3:4b-it-q4_K_M",
    "phi4-mini:3.8b-q4_K_M",
]

# Test prompts - simple code analysis prompts to generate consistent load
TEST_PROMPT = """
Analyze the following function and explain what it does:

def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
"""


class ContainerMonitor:
    """Monitor Docker containers and system resources"""

    def __init__(self, interval=1.0):
        self.interval = interval
        self.monitor = PerformanceMonitor(str(RESULTS_DIR / "raw_data"))
        self.running = False
        self.data = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def start_monitoring(self):
        """Start the monitoring process in a separate thread"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.daemon = True
        self.thread.start()

    def _monitor_loop(self):
        """Main monitoring loop that collects data at regular intervals"""
        while self.running:
            snapshot = self.monitor.capture_performance_snapshot()
            self.data.append(snapshot)
            time.sleep(self.interval)

    def stop_monitoring(self):
        """Stop the monitoring process"""
        self.running = False
        if hasattr(self, "thread"):
            self.thread.join(timeout=2.0)

        # Save collected data
        self.save_results()

    def save_results(self):
        """Save collected metrics to files and generate visualizations"""
        # Save raw data
        raw_data_file = (
            RESULTS_DIR
            / "raw_data"
            / f"performance_data_{self.timestamp}.json"
        )
        with open(raw_data_file, "w") as f:
            json.dump(self.data, f, indent=2)

        # Create and save visualizations
        self.create_visualizations()

        print(f"Saved performance data to {raw_data_file}")

    def create_visualizations(self):
        """Generate graphs from the collected data"""
        if not self.data:
            print("No data collected to visualize")
            return

        # Extract timeline data for plotting
        timestamps = [d["timestamp"] for d in self.data]
        start_time = timestamps[0]
        relative_times = [(t - start_time) for t in timestamps]

        cpu_values = [d["system"]["cpu_percent"] for d in self.data]
        memory_values = [d["system"]["memory_percent"] for d in self.data]

        # CPU and Memory Usage over time
        plt.figure(figsize=(12, 6))
        plt.plot(relative_times, cpu_values, "b-", label="CPU Usage (%)")
        plt.plot(relative_times, memory_values, "r-", label="Memory Usage (%)")
        plt.title("System Resource Usage During Parallel Container Execution")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Usage (%)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Save the visualization
        viz_file = (
            RESULTS_DIR
            / "visualizations"
            / f"system_usage_{self.timestamp}.png"
        )
        plt.savefig(viz_file)
        plt.close()

        # Create GPU usage visualization if GPU data is available
        gpu_data_available = False
        for d in self.data:
            if "gpu" in d and "devices" in d["gpu"] and d["gpu"]["devices"]:
                gpu_data_available = True
                break

        if gpu_data_available:
            # Get the number of GPUs
            num_gpus = max(
                [
                    len(d["gpu"]["devices"])
                    for d in self.data
                    if "gpu" in d and "devices" in d["gpu"]
                ]
            )

            # Create GPU utilization chart
            plt.figure(figsize=(12, 6))
            for gpu_idx in range(num_gpus):
                gpu_util_values = []
                gpu_times = []

                for i, d in enumerate(self.data):
                    if (
                        "gpu" in d
                        and "devices" in d["gpu"]
                        and len(d["gpu"]["devices"]) > gpu_idx
                    ):
                        gpu_util_values.append(
                            d["gpu"]["devices"][gpu_idx]["gpu_util_percent"]
                        )
                        gpu_times.append(relative_times[i])

                if gpu_util_values:
                    plt.plot(
                        gpu_times,
                        gpu_util_values,
                        "-",
                        label=f"GPU {gpu_idx} Utilization (%)",
                    )

            plt.title("GPU Utilization During Parallel Container Execution")
            plt.xlabel("Time (seconds)")
            plt.ylabel("GPU Utilization (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            # Save the GPU visualization
            gpu_viz_file = (
                RESULTS_DIR
                / "visualizations"
                / f"gpu_usage_{self.timestamp}.png"
            )
            plt.savefig(gpu_viz_file)
            plt.close()

            # Create VRAM usage chart
            plt.figure(figsize=(12, 6))
            for gpu_idx in range(num_gpus):
                vram_usage_values = []
                vram_times = []

                for i, d in enumerate(self.data):
                    if (
                        "gpu" in d
                        and "devices" in d["gpu"]
                        and len(d["gpu"]["devices"]) > gpu_idx
                    ):
                        vram_usage_values.append(
                            d["gpu"]["devices"][gpu_idx]["mem_used_percent"]
                        )
                        vram_times.append(relative_times[i])

                if vram_usage_values:
                    plt.plot(
                        vram_times,
                        vram_usage_values,
                        "-",
                        label=f"GPU {gpu_idx} VRAM Usage (%)",
                    )

            plt.title(
                "GPU Memory (VRAM) Usage During Parallel Container Execution"
            )
            plt.xlabel("Time (seconds)")
            plt.ylabel("VRAM Usage (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            # Save the VRAM visualization
            vram_viz_file = (
                RESULTS_DIR
                / "visualizations"
                / f"vram_usage_{self.timestamp}.png"
            )
            plt.savefig(vram_viz_file)
            plt.close()

        # If we have container-specific data, create per-container graphs
        container_names = set()
        for d in self.data:
            container_names.update(d["containers"].keys())

        if container_names:
            container_data = {
                name: {"cpu": [], "memory": [], "times": []}
                for name in container_names
            }

            for i, d in enumerate(self.data):
                for name in container_names:
                    if name in d["containers"]:
                        container_data[name]["cpu"].append(
                            d["containers"][name]["cpu_percent"]
                        )
                        container_data[name]["memory"].append(
                            d["containers"][name]["memory_usage_mb"]
                        )
                        container_data[name]["times"].append(relative_times[i])

            # Create per-container resource usage graph
            plt.figure(figsize=(12, 8))
            for name, data in container_data.items():
                if data["times"]:  # Only plot if we have data
                    plt.plot(
                        data["times"],
                        data["cpu"],
                        "-",
                        label=f"{name} CPU (%)",
                    )

            plt.title("Container CPU Usage During Parallel Execution")
            plt.xlabel("Time (seconds)")
            plt.ylabel("CPU Usage (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            # Save the container visualization
            container_viz_file = (
                RESULTS_DIR
                / "visualizations"
                / f"container_cpu_{self.timestamp}.png"
            )
            plt.savefig(container_viz_file)
            plt.close()

            # Memory usage graph
            plt.figure(figsize=(12, 8))
            for name, data in container_data.items():
                if data["times"]:  # Only plot if we have data
                    plt.plot(
                        data["times"],
                        data["memory"],
                        "-",
                        label=f"{name} Memory (MB)",
                    )

            plt.title("Container Memory Usage During Parallel Execution")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Memory Usage (MB)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            container_mem_viz_file = (
                RESULTS_DIR
                / "visualizations"
                / f"container_memory_{self.timestamp}.png"
            )
            plt.savefig(container_mem_viz_file)
            plt.close()


def run_container(model_name, prompt, container_name=None):
    """Run a Docker container with the specified model"""
    client = docker.from_env()

    # Generate unique container name if not provided
    if not container_name:
        container_name = (
            f"ollama-test-{model_name.split(':')[0]}-{time.time()}"
        )

    # Ollama model volume
    models_volume = os.path.abspath("../../ollama-models")
    os.makedirs(models_volume, exist_ok=True)

    try:
        # Start the container
        container = client.containers.run(
            "ollama/ollama",
            name=container_name,
            ports={"11434/tcp": None},  # Automatically assign port
            volumes={models_volume: {"bind": "/root/.ollama", "mode": "rw"}},
            detach=True,
            remove=True,
        )

        print(f"Started container {container_name} running model {model_name}")

        # Wait for API to become available
        port = client.api.port(container.id, 11434)[0]["HostPort"]
        time.sleep(5)  # Simple wait for the container to initialize

        # For extended testing, you could add code here to query the model

        return container, port

    except Exception as e:
        print(f"Error starting container for {model_name}: {e}")
        return None, None


def run_parallel_test(models=None, duration=60):
    """
    Run multiple containers in parallel and measure performance
    
    Args:
        models: List of model names to test in parallel
        duration: How long to run the test in seconds
    """
    if models is None:
        models = MODELS[:3]  # Default to testing 3 models in parallel

    print(f"Starting parallel test with {len(models)} containers")
    print(f"Models: {', '.join(models)}")

    # Start performance monitoring
    monitor = ContainerMonitor(interval=1.0)
    monitor.start_monitoring()

    containers = []
    try:
        # Start containers in parallel
        for i, model in enumerate(models):
            container_name = f"ollama-test-{i+1}"
            container, port = run_container(model, TEST_PROMPT, container_name)
            if container:
                containers.append(container)

        print(f"Started {len(containers)} containers successfully")
        print(f"Monitoring for {duration} seconds...")

        # Keep containers running for the specified duration
        time.sleep(duration)

    finally:
        # Stop monitoring and save results
        monitor.stop_monitoring()

        # Stop and remove all containers
        print("Stopping containers...")
        for container in containers:
            try:
                container.stop(timeout=5)
                print(f"Stopped container {container.name}")
            except Exception as e:
                print(f"Error stopping container {container.name}: {e}")

    # Generate a summary report
    summary_file = (
        RESULTS_DIR / "raw_data" / f"summary_{monitor.timestamp}.txt"
    )
    with open(summary_file, "w") as f:
        f.write("Container Parallel Performance Test Summary\n")
        f.write("========================================\n\n")
        f.write(
            f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        f.write(f"Duration: {duration} seconds\n")
        f.write(f"Models tested: {', '.join(models)}\n\n")

        # Calculate averages
        cpu_avg = (
            sum(d["system"]["cpu_percent"] for d in monitor.data)
            / len(monitor.data)
            if monitor.data
            else 0
        )
        mem_avg = (
            sum(d["system"]["memory_percent"] for d in monitor.data)
            / len(monitor.data)
            if monitor.data
            else 0
        )

        f.write(f"Average CPU usage: {cpu_avg:.2f}%\n")
        f.write(f"Average Memory usage: {mem_avg:.2f}%\n\n")

        f.write("Container stats:\n")
        container_names = set()
        for d in monitor.data:
            container_names.update(d["containers"].keys())

        for name in container_names:
            container_data = []
            for d in monitor.data:
                if name in d["containers"]:
                    container_data.append(d["containers"][name])

            if container_data:
                cpu_avg = sum(c["cpu_percent"] for c in container_data) / len(
                    container_data
                )
                mem_avg = sum(
                    c["memory_usage_mb"] for c in container_data
                ) / len(container_data)

                f.write(f"  {name}:\n")
                f.write(f"    CPU Avg: {cpu_avg:.2f}%\n")
                f.write(f"    Memory Avg: {mem_avg:.2f} MB\n")

    print(f"Testing completed! Results saved in {RESULTS_DIR}")
    return monitor.data


if __name__ == "__main__":
    # Test with different scenarios

    # Test 1: Run all models in parallel
    print("Running test with all models in parallel...")
    run_parallel_test(MODELS, duration=120)

    # Test 2: Run a single model to establish baseline
    print("\nRunning baseline test with a single model...")
    run_parallel_test([MODELS[0]], duration=60)

    # Test 3: Run models in batches (3 at a time)
    print("\nRunning test with 3 models in parallel...")
    run_parallel_test(MODELS[:3], duration=90)
