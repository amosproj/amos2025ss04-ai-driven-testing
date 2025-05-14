#!/usr/bin/env python3
"""
Visualization module for performance metrics collected by the performance_monitor module.

This module provides functions for generating visualizations of CPU, memory, and GPU usage
based on the data collected during performance testing.
"""

import os
import json
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime


class PerformanceVisualizer:
    """Generates visualizations from performance test data"""

    def __init__(self, output_dir=None):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # Default location is 'performance_results' in the current directory
            self.output_dir = (
                Path(os.path.dirname(os.path.abspath(__file__)))
                / "performance_results"
            )

        # Create output directories if they don't exist
        self.viz_dir = self.output_dir / "visualizations"
        self.viz_dir.mkdir(exist_ok=True, parents=True)

    def create_visualizations(self, performance_data, prefix=None):
        """
        Create visualizations from performance test data

        Args:
            performance_data: List of performance snapshots or path to JSON file
            prefix: Optional prefix for output filenames

        Returns:
            Dict of generated visualization paths
        """
        # Load data from file if a string path is provided
        if isinstance(performance_data, (str, Path)):
            with open(performance_data, "r") as f:
                performance_data = json.load(f)

        # Check if it's a list of snapshots or a single performance test result
        if isinstance(performance_data, list):
            return self._create_time_series_visualizations(
                performance_data, prefix
            )
        else:
            return self._create_before_after_visualizations(
                performance_data, prefix
            )

    def _create_time_series_visualizations(self, snapshots, prefix=None):
        """Generate visualizations for a time series of performance snapshots"""
        if not snapshots:
            print("No data to visualize")
            return {}

        # Extract timeline data for plotting
        timestamps = [d["timestamp"] for d in snapshots]
        start_time = timestamps[0]
        relative_times = [(t - start_time) for t in timestamps]

        # CPU and Memory Usage over time
        cpu_values = [d["system"]["cpu_percent"] for d in snapshots]
        memory_values = [d["system"]["memory_percent"] for d in snapshots]

        # Generate visualizations
        viz_paths = {}

        # Prepare filename prefix
        file_prefix = f"{prefix}_" if prefix else ""

        # System resource usage (CPU + Memory)
        plt.figure(figsize=(12, 6))
        plt.plot(relative_times, cpu_values, "b-", label="CPU Usage (%)")
        plt.plot(relative_times, memory_values, "r-", label="Memory Usage (%)")
        plt.title("System Resource Usage During Performance Test")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Usage (%)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        system_viz_path = (
            self.viz_dir / f"{file_prefix}system_usage_{self.timestamp}.png"
        )
        plt.savefig(system_viz_path)
        plt.close()
        viz_paths["system"] = str(system_viz_path)

        # Create GPU usage visualization if GPU data is available
        gpu_data_available = False
        for d in snapshots:
            if "gpu" in d and "devices" in d["gpu"] and d["gpu"]["devices"]:
                gpu_data_available = True
                break

        if gpu_data_available:
            # Get the number of GPUs
            num_gpus = max(
                [
                    len(d["gpu"]["devices"])
                    for d in snapshots
                    if "gpu" in d and "devices" in d["gpu"]
                ]
            )

            # Create GPU utilization chart
            plt.figure(figsize=(12, 6))
            for gpu_idx in range(num_gpus):
                gpu_util_values = []
                gpu_times = []

                for i, d in enumerate(snapshots):
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

            plt.title("GPU Utilization During Performance Test")
            plt.xlabel("Time (seconds)")
            plt.ylabel("GPU Utilization (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            gpu_viz_path = (
                self.viz_dir / f"{file_prefix}gpu_usage_{self.timestamp}.png"
            )
            plt.savefig(gpu_viz_path)
            plt.close()
            viz_paths["gpu"] = str(gpu_viz_path)

            # Create VRAM usage chart
            plt.figure(figsize=(12, 6))
            for gpu_idx in range(num_gpus):
                vram_usage_values = []
                vram_times = []

                for i, d in enumerate(snapshots):
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

            plt.title("GPU Memory (VRAM) Usage During Performance Test")
            plt.xlabel("Time (seconds)")
            plt.ylabel("VRAM Usage (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            vram_viz_path = (
                self.viz_dir / f"{file_prefix}vram_usage_{self.timestamp}.png"
            )
            plt.savefig(vram_viz_path)
            plt.close()
            viz_paths["vram"] = str(vram_viz_path)

        # Container-specific usage if container data is available
        container_names = set()
        for d in snapshots:
            container_names.update(d["containers"].keys())

        if container_names:
            container_data = {
                name: {"cpu": [], "memory": [], "times": []}
                for name in container_names
            }

            for i, d in enumerate(snapshots):
                for name in container_names:
                    if name in d["containers"]:
                        container_data[name]["cpu"].append(
                            d["containers"][name]["cpu_percent"]
                        )
                        container_data[name]["memory"].append(
                            d["containers"][name]["memory_usage_mb"]
                        )
                        container_data[name]["times"].append(relative_times[i])

            # Create per-container CPU usage graph
            plt.figure(figsize=(12, 8))
            for name, data in container_data.items():
                if data["times"]:  # Only plot if we have data
                    plt.plot(
                        data["times"],
                        data["cpu"],
                        "-",
                        label=f"{name} CPU (%)",
                    )

            plt.title("Container CPU Usage During Performance Test")
            plt.xlabel("Time (seconds)")
            plt.ylabel("CPU Usage (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            container_cpu_path = (
                self.viz_dir
                / f"{file_prefix}container_cpu_{self.timestamp}.png"
            )
            plt.savefig(container_cpu_path)
            plt.close()
            viz_paths["container_cpu"] = str(container_cpu_path)

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

            plt.title("Container Memory Usage During Performance Test")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Memory Usage (MB)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            container_mem_path = (
                self.viz_dir
                / f"{file_prefix}container_memory_{self.timestamp}.png"
            )
            plt.savefig(container_mem_path)
            plt.close()
            viz_paths["container_memory"] = str(container_mem_path)

        return viz_paths

    def _create_before_after_visualizations(self, perf_data, prefix=None):
        """Generate before-after comparison visualizations"""
        viz_paths = {}

        # Check that we have before/after metrics
        if not (
            "system_metrics" in perf_data
            and "before" in perf_data["system_metrics"]
            and "after" in perf_data["system_metrics"]
        ):
            print("Missing before/after system metrics data")
            return {}

        # Prepare filename prefix
        file_prefix = f"{prefix}_" if prefix else ""

        # System metrics comparison
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # CPU usage comparison
        cpu_labels = ["Before", "After"]
        cpu_values = [
            perf_data["system_metrics"]["before"]["cpu_percent"],
            perf_data["system_metrics"]["after"]["cpu_percent"],
        ]
        ax1.bar(cpu_labels, cpu_values, color=["blue", "red"])
        ax1.set_ylabel("CPU Usage (%)")
        ax1.set_title("CPU Usage Before vs After")
        ax1.grid(axis="y", linestyle="--", alpha=0.7)

        # Memory usage comparison
        mem_labels = ["Before", "After"]
        mem_values = [
            perf_data["system_metrics"]["before"]["memory_percent"],
            perf_data["system_metrics"]["after"]["memory_percent"],
        ]
        ax2.bar(mem_labels, mem_values, color=["blue", "red"])
        ax2.set_ylabel("Memory Usage (%)")
        ax2.set_title("Memory Usage Before vs After")
        ax2.grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()
        system_comparison_path = (
            self.viz_dir
            / f"{file_prefix}system_comparison_{self.timestamp}.png"
        )
        plt.savefig(system_comparison_path)
        plt.close()
        viz_paths["system_comparison"] = str(system_comparison_path)

        # GPU comparison if available
        if (
            "gpu_metrics" in perf_data
            and "before" in perf_data["gpu_metrics"]
            and "after" in perf_data["gpu_metrics"]
        ):
            if (
                "devices" in perf_data["gpu_metrics"]["before"]
                and "devices" in perf_data["gpu_metrics"]["after"]
                and perf_data["gpu_metrics"]["before"]["devices"]
                and perf_data["gpu_metrics"]["after"]["devices"]
            ):

                # GPU utilization comparison for each GPU
                num_gpus = min(
                    len(perf_data["gpu_metrics"]["before"]["devices"]),
                    len(perf_data["gpu_metrics"]["after"]["devices"]),
                )

                fig, axes = plt.subplots(
                    num_gpus, 2, figsize=(12, num_gpus * 4)
                )
                if num_gpus == 1:
                    axes = [axes]  # Make 2D for consistent indexing

                for i in range(num_gpus):
                    before_gpu = perf_data["gpu_metrics"]["before"]["devices"][
                        i
                    ]
                    after_gpu = perf_data["gpu_metrics"]["after"]["devices"][i]

                    # GPU utilization
                    gpu_labels = ["Before", "After"]
                    gpu_values = [
                        before_gpu["gpu_util_percent"],
                        after_gpu["gpu_util_percent"],
                    ]
                    axes[i][0].bar(
                        gpu_labels, gpu_values, color=["blue", "red"]
                    )
                    axes[i][0].set_ylabel("GPU Utilization (%)")
                    axes[i][0].set_title(
                        f"GPU {i} Utilization Before vs After"
                    )
                    axes[i][0].grid(axis="y", linestyle="--", alpha=0.7)

                    # VRAM usage
                    vram_labels = ["Before", "After"]
                    vram_values = [
                        before_gpu["mem_used_percent"],
                        after_gpu["mem_used_percent"],
                    ]
                    axes[i][1].bar(
                        vram_labels, vram_values, color=["blue", "red"]
                    )
                    axes[i][1].set_ylabel("VRAM Usage (%)")
                    axes[i][1].set_title(f"GPU {i} VRAM Usage Before vs After")
                    axes[i][1].grid(axis="y", linestyle="--", alpha=0.7)

                plt.tight_layout()
                gpu_comparison_path = (
                    self.viz_dir
                    / f"{file_prefix}gpu_comparison_{self.timestamp}.png"
                )
                plt.savefig(gpu_comparison_path)
                plt.close()
                viz_paths["gpu_comparison"] = str(gpu_comparison_path)

        return viz_paths

    def generate_summary_report(self, performance_data, output_file=None):
        """
        Generate a text summary report of performance metrics

        Args:
            performance_data: Performance data dict or path to JSON file
            output_file: Optional file path to save the report

        Returns:
            String containing the summary report
        """
        # Load data from file if a string path is provided
        if isinstance(performance_data, (str, Path)):
            with open(performance_data, "r") as f:
                performance_data = json.load(f)

        # Check if it's time series data or a before-after comparison
        if isinstance(performance_data, list):
            report = self._generate_time_series_report(performance_data)
        else:
            report = self._generate_before_after_report(performance_data)

        # Save the report if an output file is specified
        if output_file:
            with open(output_file, "w") as f:
                f.write(report)

        return report

    def _generate_time_series_report(self, snapshots):
        """Generate a report for time series performance data"""
        report = []
        report.append("PERFORMANCE TEST SUMMARY REPORT")
        report.append("=============================\n")
        report.append(
            f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report.append(
            f"Test Duration: {snapshots[-1]['timestamp'] - snapshots[0]['timestamp']:.2f} seconds"
        )
        report.append(f"Number of Samples: {len(snapshots)}\n")

        # System metrics
        cpu_avg = sum(d["system"]["cpu_percent"] for d in snapshots) / len(
            snapshots
        )
        cpu_max = max(d["system"]["cpu_percent"] for d in snapshots)
        mem_avg = sum(d["system"]["memory_percent"] for d in snapshots) / len(
            snapshots
        )
        mem_max = max(d["system"]["memory_percent"] for d in snapshots)

        report.append("SYSTEM RESOURCE USAGE:")
        report.append(f"  CPU Average: {cpu_avg:.2f}%")
        report.append(f"  CPU Peak: {cpu_max:.2f}%")
        report.append(f"  Memory Average: {mem_avg:.2f}%")
        report.append(f"  Memory Peak: {mem_max:.2f}%")

        # GPU metrics if available
        gpu_data_available = False
        for d in snapshots:
            if "gpu" in d and "devices" in d["gpu"] and d["gpu"]["devices"]:
                gpu_data_available = True
                break

        if gpu_data_available:
            report.append("\nGPU RESOURCE USAGE:")

            # Determine number of GPUs
            num_gpus = max(
                [
                    len(d["gpu"]["devices"])
                    for d in snapshots
                    if "gpu" in d and "devices" in d["gpu"]
                ]
            )

            for gpu_idx in range(num_gpus):
                gpu_util_values = []
                vram_values = []

                for d in snapshots:
                    if (
                        "gpu" in d
                        and "devices" in d["gpu"]
                        and len(d["gpu"]["devices"]) > gpu_idx
                    ):
                        gpu_util_values.append(
                            d["gpu"]["devices"][gpu_idx]["gpu_util_percent"]
                        )
                        vram_values.append(
                            d["gpu"]["devices"][gpu_idx]["mem_used_percent"]
                        )

                if gpu_util_values:
                    gpu_util_avg = sum(gpu_util_values) / len(gpu_util_values)
                    gpu_util_max = max(gpu_util_values)
                    vram_avg = sum(vram_values) / len(vram_values)
                    vram_max = max(vram_values)

                    report.append(f"  GPU {gpu_idx}:")
                    report.append(
                        f"    Utilization Average: {gpu_util_avg:.2f}%"
                    )
                    report.append(f"    Utilization Peak: {gpu_util_max:.2f}%")
                    report.append(f"    VRAM Usage Average: {vram_avg:.2f}%")
                    report.append(f"    VRAM Usage Peak: {vram_max:.2f}%")

        # Container metrics
        container_names = set()
        for d in snapshots:
            container_names.update(d["containers"].keys())

        if container_names:
            report.append("\nCONTAINER RESOURCE USAGE:")

            for name in container_names:
                container_data = []

                for d in snapshots:
                    if name in d["containers"]:
                        container_data.append(d["containers"][name])

                if container_data:
                    cpu_avg = sum(
                        c["cpu_percent"] for c in container_data
                    ) / len(container_data)
                    cpu_max = max(c["cpu_percent"] for c in container_data)
                    mem_avg = sum(
                        c["memory_usage_mb"] for c in container_data
                    ) / len(container_data)
                    mem_max = max(c["memory_usage_mb"] for c in container_data)

                    report.append(f"  {name}:")
                    report.append(f"    CPU Average: {cpu_avg:.2f}%")
                    report.append(f"    CPU Peak: {cpu_max:.2f}%")
                    report.append(f"    Memory Average: {mem_avg:.2f} MB")
                    report.append(f"    Memory Peak: {mem_max:.2f} MB")

        return "\n".join(report)

    def _generate_before_after_report(self, perf_data):
        """Generate a report for before-after performance comparison"""
        report = []
        report.append("PERFORMANCE TEST COMPARISON REPORT")
        report.append("================================\n")
        report.append(
            f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        # System metrics
        if "system_metrics" in perf_data:
            report.append("SYSTEM RESOURCE USAGE:")
            report.append(
                f"  CPU Before: {perf_data['system_metrics']['before']['cpu_percent']:.2f}%"
            )
            report.append(
                f"  CPU After: {perf_data['system_metrics']['after']['cpu_percent']:.2f}%"
            )
            report.append(
                f"  CPU Delta: {perf_data['system_metrics']['cpu_delta']:.2f}%"
            )
            report.append(
                f"  Memory Before: {perf_data['system_metrics']['before']['memory_percent']:.2f}%"
            )
            report.append(
                f"  Memory After: {perf_data['system_metrics']['after']['memory_percent']:.2f}%"
            )
            report.append(
                f"  Memory Delta: {perf_data['system_metrics']['after']['memory_percent'] - perf_data['system_metrics']['before']['memory_percent']:.2f}%"
            )

        # GPU metrics
        if "gpu_metrics" in perf_data and "deltas" in perf_data["gpu_metrics"]:
            report.append("\nGPU RESOURCE USAGE:")

            for i, gpu in enumerate(perf_data["gpu_metrics"]["deltas"]):
                report.append(f"  GPU {gpu['index']}:")
                report.append(
                    f"    Utilization Delta: {gpu['gpu_util_delta']:.2f}%"
                )
                report.append(
                    f"    VRAM Usage Delta: {gpu['mem_used_delta_mb']:.2f} MB"
                )
                report.append(
                    f"    VRAM Usage % Delta: {gpu['mem_used_percent_delta']:.2f}%"
                )

        # Container metrics
        if "container_metrics" in perf_data:
            before_containers = perf_data["container_metrics"]["before"]
            after_containers = perf_data["container_metrics"]["after"]

            if before_containers or after_containers:
                report.append("\nCONTAINER RESOURCE USAGE:")

                # All container names (before and after)
                container_names = set(before_containers.keys()) | set(
                    after_containers.keys()
                )

                for name in container_names:
                    report.append(f"  {name}:")

                    # Container might only exist in before or after
                    if name in before_containers and name in after_containers:
                        cpu_before = before_containers[name]["cpu_percent"]
                        cpu_after = after_containers[name]["cpu_percent"]
                        mem_before = before_containers[name]["memory_usage_mb"]
                        mem_after = after_containers[name]["memory_usage_mb"]

                        report.append(f"    CPU Before: {cpu_before:.2f}%")
                        report.append(f"    CPU After: {cpu_after:.2f}%")
                        report.append(
                            f"    CPU Delta: {cpu_after - cpu_before:.2f}%"
                        )
                        report.append(
                            f"    Memory Before: {mem_before:.2f} MB"
                        )
                        report.append(f"    Memory After: {mem_after:.2f} MB")
                        report.append(
                            f"    Memory Delta: {mem_after - mem_before:.2f} MB"
                        )
                    elif name in before_containers:
                        report.append("    Container only present before test")
                        report.append(
                            f"    CPU: {before_containers[name]['cpu_percent']:.2f}%"
                        )
                        report.append(
                            f"    Memory: {before_containers[name]['memory_usage_mb']:.2f} MB"
                        )
                    else:
                        report.append("    Container only present after test")
                        report.append(
                            f"    CPU: {after_containers[name]['cpu_percent']:.2f}%"
                        )
                        report.append(
                            f"    Memory: {after_containers[name]['memory_usage_mb']:.2f} MB"
                        )

        return "\n".join(report)
