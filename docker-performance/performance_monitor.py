"""Performance monitoring module for Docker containers and system resources.

This module provides utilities for monitoring Docker container performance and
system resource usage. It can track CPU, memory, GPU, VRAM, and other metrics for both
the host system and individual containers.
"""

import time
import json
import psutil
import docker
import subprocess
import shutil
from pathlib import Path


class PerformanceMonitor:
    """Monitor Docker containers and system resources including GPU metrics"""

    def __init__(self, output_dir=None):
        self.docker_client = docker.from_env()
        self.output_dir = output_dir
        if output_dir:
            Path(output_dir).mkdir(exist_ok=True)
        # Check if nvidia-smi is available for GPU monitoring
        self.has_nvidia_gpu = self._check_nvidia_smi()

    def _check_nvidia_smi(self):
        """Check if nvidia-smi is available on the system"""
        return shutil.which("nvidia-smi") is not None

    def get_gpu_metrics(self):
        """Get current GPU resource usage metrics using nvidia-smi"""
        if not self.has_nvidia_gpu:
            return {
                "error": "No NVIDIA GPU detected or nvidia-smi not available"
            }

        try:
            # Get GPU utilization
            gpu_util_output = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu,utilization.memory,memory.total,memory.used,memory.free",
                    "--format=csv,noheader,nounits",
                ],
                universal_newlines=True,
            )

            # Parse the output
            gpu_metrics = []
            for i, line in enumerate(gpu_util_output.strip().split("\n")):
                values = line.split(", ")
                if len(values) >= 5:
                    gpu_util = float(values[0])
                    mem_util = float(values[1])
                    mem_total = float(values[2])
                    mem_used = float(values[3])
                    mem_free = float(values[4])

                    gpu_metrics.append(
                        {
                            "index": i,
                            "gpu_util_percent": gpu_util,
                            "mem_util_percent": mem_util,
                            "mem_total_mb": mem_total,
                            "mem_used_mb": mem_used,
                            "mem_free_mb": mem_free,
                            "mem_used_percent": (
                                (mem_used / mem_total) * 100
                                if mem_total > 0
                                else 0
                            ),
                        }
                    )

            return {"devices": gpu_metrics, "count": len(gpu_metrics)}

        except (subprocess.SubprocessError, ValueError) as e:
            return {"error": f"Failed to get GPU metrics: {str(e)}"}

    def get_system_metrics(self):
        """Get current system resource usage metrics"""
        metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_gb": round(
                psutil.virtual_memory().used / (1024**3), 2
            ),
            "memory_total_gb": round(
                psutil.virtual_memory().total / (1024**3), 2
            ),
            "swap_percent": psutil.swap_memory().percent,
            "swap_used_gb": round(psutil.swap_memory().used / (1024**3), 2),
            "timestamp": time.time(),
        }
        return metrics

    def calculate_cpu_percent(self, stats):
        """Calculate CPU percent usage from Docker stats"""
        try:
            cpu_delta = (
                stats["cpu_stats"]["cpu_usage"]["total_usage"]
                - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            )
            system_delta = (
                stats["cpu_stats"]["system_cpu_usage"]
                - stats["precpu_stats"]["system_cpu_usage"]
            )
            if system_delta > 0 and cpu_delta > 0:
                return round(
                    (cpu_delta / system_delta)
                    * len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"])
                    * 100,
                    2,
                )
            return 0.0
        except (KeyError, ZeroDivisionError):
            return 0.0

    def monitor_docker_containers(self):
        """Get metrics for all running Docker containers"""
        try:
            container_stats = {}

            for container in self.docker_client.containers.list():
                stats = container.stats(stream=False)
                container_stats[container.name] = {
                    "id": container.id[:12],
                    "name": container.name,
                    "cpu_percent": self.calculate_cpu_percent(stats),
                    "memory_usage_mb": round(
                        stats["memory_stats"].get("usage", 0) / (1024**2), 2
                    ),
                    "memory_limit_mb": round(
                        stats["memory_stats"].get("limit", 0) / (1024**2), 2
                    ),
                    "memory_percent": round(
                        (
                            stats["memory_stats"].get("usage", 0)
                            / stats["memory_stats"].get("limit", 1)
                        )
                        * 100,
                        2,
                    ),
                    "image": (
                        container.image.tags[0]
                        if container.image.tags
                        else "unknown"
                    ),
                }

                # Add GPU metrics for containers if using nvidia-docker
                if self.has_nvidia_gpu:
                    try:
                        # Check for GPU device assignments - this requires additional permissions
                        # and may not work in all environments
                        inspect = self.docker_client.api.inspect_container(
                            container.id
                        )
                        if "NvidiaRuntime" in str(inspect) or "nvidia" in str(
                            inspect
                        ):
                            container_stats[container.name]["uses_gpu"] = True
                    except:
                        pass

            return container_stats
        except Exception as e:
            print(f"Error monitoring Docker containers: {e}")
            return {}

    def capture_performance_snapshot(self):
        """Capture a snapshot of current system and container performance including GPU metrics"""
        snapshot = {
            "system": self.get_system_metrics(),
            "containers": self.monitor_docker_containers(),
            "timestamp": time.time(),
        }

        # Add GPU metrics if available
        if self.has_nvidia_gpu:
            snapshot["gpu"] = self.get_gpu_metrics()

        return snapshot

    def save_performance_metrics(
        self, metrics, filename="docker_performance.json"
    ):
        """Save performance metrics to a JSON file"""
        if self.output_dir:
            file_path = Path(self.output_dir) / filename
        else:
            file_path = Path(filename)

        with open(file_path, "w") as f:
            json.dump(metrics, f, indent=2)

        return str(file_path)


def capture_performance_before_after(func, *args, output_file=None, **kwargs):
    """
    Decorator-like function that captures performance before and after executing a function

    Args:
        func: The function to execute and measure
        *args: Arguments to pass to the function
        output_file: Optional file to save performance metrics
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Tuple of (function result, performance metrics dict)
    """
    monitor = PerformanceMonitor()

    # Capture baseline performance
    baseline = monitor.capture_performance_snapshot()

    # Execute the function
    result = func(*args, **kwargs)

    # Capture post-execution performance
    post_execution = monitor.capture_performance_snapshot()

    # Compile performance metrics
    performance_data = {
        "timestamp": time.time(),
        "system_metrics": {
            "before": baseline["system"],
            "after": post_execution["system"],
            "cpu_delta": post_execution["system"]["cpu_percent"]
            - baseline["system"]["cpu_percent"],
            "memory_delta_gb": round(
                post_execution["system"]["memory_used_gb"]
                - baseline["system"]["memory_used_gb"],
                2,
            ),
        },
        "container_metrics": {
            "before": baseline["containers"],
            "after": post_execution["containers"],
        },
    }

    # Add GPU metrics if available
    if "gpu" in baseline and "gpu" in post_execution:
        performance_data["gpu_metrics"] = {
            "before": baseline["gpu"],
            "after": post_execution["gpu"],
        }

        # Calculate GPU utilization delta if we have valid metrics
        if "devices" in baseline["gpu"] and "devices" in post_execution["gpu"]:
            # Only process if we actually have gpu devices
            if baseline["gpu"]["devices"] and post_execution["gpu"]["devices"]:
                gpu_deltas = []
                for i in range(
                    min(
                        len(baseline["gpu"]["devices"]),
                        len(post_execution["gpu"]["devices"]),
                    )
                ):
                    before_device = baseline["gpu"]["devices"][i]
                    after_device = post_execution["gpu"]["devices"][i]
                    gpu_deltas.append(
                        {
                            "index": i,
                            "gpu_util_delta": after_device["gpu_util_percent"]
                            - before_device["gpu_util_percent"],
                            "mem_used_delta_mb": after_device["mem_used_mb"]
                            - before_device["mem_used_mb"],
                            "mem_used_percent_delta": after_device[
                                "mem_used_percent"
                            ]
                            - before_device["mem_used_percent"],
                        }
                    )
                performance_data["gpu_metrics"]["deltas"] = gpu_deltas

    # Save metrics if an output file is provided
    if output_file:
        monitor.save_performance_metrics(performance_data, output_file)

    return result, performance_data
