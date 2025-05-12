#!/usr/bin/env python3
"""
Docker Container Performance Testing for LLM Models

This script runs performance tests on Docker containers for LLM models to determine
if they can run in parallel or need to be stopped after use. It uses the LLMManager
to handle container lifecycle and integrates with performance monitoring tools.

Example usage:
    python3 run_performance_test.py --mode parallel --models mistral:7b deepseek:6.7b
    python3 run_performance_test.py --mode sequential --prompt-file test_prompt.txt
    python3 run_performance_test.py --mode benchmark --duration 120
"""

import os
import sys
import time
import json
import threading
import argparse
from pathlib import Path
from datetime import datetime
import importlib.util

# Add the parent directory to the Python path so we can import from backend
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

# Check if module exists before importing
try:
    from backend.llm_manager import LLMManager
except ImportError:
    print("Error: llm_manager.py not found or could not be imported.")
    print("Make sure backend/llm_manager.py exists and is importable.")
    sys.exit(1)

from performance_monitor import PerformanceMonitor
from performance_visualization import PerformanceVisualizer

# Constants
BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "backend")
)
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(THIS_DIR, "performance_results")
PROMPT_FILE = os.path.join(THIS_DIR, "prompt.txt")
CONFIG_FILE = os.path.join(BACKEND_DIR, "allowed_models.json")


def get_allowed_models():
    """Get the list of allowed models from the config file"""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [model_info["id"] for model_info in data.get("models", [])]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading config file: {e}")
        return []


def create_or_load_allowed_models_file():
    """Create the allowed models file if it doesn't exist"""
    if not os.path.exists(CONFIG_FILE):
        print(f"Error loading allowed_models.json: File not found.")
        return []
    else:
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("models", [])
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading allowed_models.json: {e}")
            return []


def load_prompt(prompt_file=None):
    """Load the prompt from a file"""
    if prompt_file and os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        raise FileNotFoundError("The specified file was not found.")


class PerformanceTest:
    """Runs performance tests on LLM containers"""

    def __init__(self, output_dir=None):
        self.llm_manager = LLMManager()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create a base directory for results
        self.base_results_dir = Path(output_dir or RESULTS_DIR)
        self.base_results_dir.mkdir(exist_ok=True, parents=True)

        # Create a timestamped directory for this specific run
        self.results_dir = self.base_results_dir / f"run_{self.timestamp}"
        self.results_dir.mkdir(exist_ok=True, parents=True)

        # Create raw_data subdirectory
        self.raw_data_dir = self.results_dir / "raw_data"
        self.raw_data_dir.mkdir(exist_ok=True, parents=True)

        # Initialize monitor and visualizer with the new directory structure
        self.monitor = PerformanceMonitor(output_dir=str(self.raw_data_dir))
        self.visualizer = PerformanceVisualizer(
            output_dir=str(self.results_dir)
        )

        print(
            f"\nResults for this test run will be saved to: {self.results_dir}"
        )

    def run_sequential_test(self, models, prompt):
        """
        Run models sequentially and measure performance

        Args:
            models: List of model IDs to test
            prompt: Prompt to send to each model

        Returns:
            Dictionary with test results
        """
        print(f"\nRunning sequential test with {len(models)} models")
        print(f"Running each model sequentially\n")

        all_model_data = []

        for model_id in models:
            print(f"\n{'='*50}")
            print(f"Testing model: {model_id}")
            print(f"{'='*50}")

            # Start collecting performance data
            performance_data = []
            monitor_thread = self._start_monitoring(
                performance_data, interval=1.0
            )

            try:
                # Start the container
                self.llm_manager.start_model_container(model_id)
                print(f"Started container for {model_id}")

                # Send the prompt
                start_time = time.time()
                print(f"Sending prompt to {model_id}...")

                # Use a custom output file for this test
                output_file = f"sequential_test_{model_id.replace(':', '_')}_{self.timestamp}.md"
                self.llm_manager.send_prompt(
                    model_id, prompt, output_file=output_file
                )

            finally:
                # Stop monitoring
                self._stop_monitoring(monitor_thread)

                # Stop the container
                try:
                    self.llm_manager.stop_model_container(model_id)
                    print(f"Stopped container for {model_id}")
                except Exception as e:
                    print(f"Error stopping container for {model_id}: {e}")

            # Save this model's performance data
            model_data_file = (
                self.raw_data_dir
                / f"sequential_{model_id.replace(':', '_')}_{self.timestamp}.json"
            )
            with open(model_data_file, "w") as f:
                json.dump(performance_data, f, indent=2)

            # Generate visualizations for this model
            viz_paths = self.visualizer.create_visualizations(
                performance_data,
                prefix=f"sequential_{model_id.replace(':', '_')}",
            )

            # Generate summary report
            report = self.visualizer.generate_summary_report(
                performance_data,
                output_file=str(
                    self.raw_data_dir
                    / f"sequential_{model_id.replace(':', '_')}_{self.timestamp}_report.txt"
                ),
            )

            print(f"\nTest completed for {model_id}")
            print(f"Performance data saved to {model_data_file}")

            # Store data for overall summary
            all_model_data.append(
                {
                    "model_id": model_id,
                    "data_file": str(model_data_file),
                    "visualizations": viz_paths,
                    "report": report,
                }
            )

        # Create a summary file with links to all individual test results
        summary_file = (
            self.results_dir / f"sequential_test_summary_{self.timestamp}.json"
        )
        with open(summary_file, "w") as f:
            json.dump(
                {
                    "timestamp": self.timestamp,
                    "mode": "sequential",
                    "models_tested": models,
                    "results": all_model_data,
                },
                f,
                indent=2,
            )

        print(f"\nSequential testing completed!")
        print(f"Summary saved to {summary_file}")

        return {
            "summary_file": str(summary_file),
            "model_results": all_model_data,
        }

    def run_sequential_all_containers_test(self, models, prompt):
        """
        Run models sequentially, but with all containers started first and stopped at the end.
        This allows measuring the performance impact of idle but running containers.

        Args:
            models: List of model IDs to test
            prompt: Prompt to send to each model

        Returns:
            Dictionary with test results
        """
        print(f"\nRunning sequential test with all containers started upfront")
        print(
            f"This mode starts {len(models)} containers, then prompts each sequentially"
        )
        print(
            f"Performance is tracked for the entire duration, including idle time"
        )

        # Start collecting performance data
        performance_data = []
        monitor_thread = self._start_monitoring(performance_data, interval=1.0)

        active_models = []
        all_model_data = []

        try:
            # Start all containers first
            print("\nStarting all containers...")
            for model_id in models:
                try:
                    self.llm_manager.start_model_container(model_id)
                    print(f"Started container for {model_id}")
                    active_models.append(model_id)
                except Exception as e:
                    print(f"Error starting container for {model_id}: {e}")

            # Allow time for containers to stabilize
            print("\nWaiting for containers to stabilize...")
            time.sleep(10)

            # Now prompt each model sequentially
            for model_id in active_models:
                print(f"\n{'='*50}")
                print(f"Sending prompt to model: {model_id}")
                print(f"{'='*50}")

                # Send the prompt
                start_time = time.time()
                print(f"Sending prompt...")

                # Use a custom output file for this test
                output_file = f"sequential_all_{model_id.replace(':', '_')}_{self.timestamp}.md"

                try:
                    self.llm_manager.send_prompt(
                        model_id, prompt, output_file=output_file
                    )
                    print(f"Completed prompt processing for {model_id}")
                except Exception as e:
                    print(f"Error sending prompt to {model_id}: {e}")

                # Store data for this model
                all_model_data.append(
                    {"model_id": model_id, "output_file": output_file}
                )

            # Allow time to capture post-processing metrics
            print("\nCapturing final metrics...")
            time.sleep(5)

        finally:
            # Stop monitoring
            self._stop_monitoring(monitor_thread)

            # Stop all containers
            print("\nStopping all containers...")
            for model_id in active_models:
                try:
                    self.llm_manager.stop_model_container(model_id)
                    print(f"Stopped container for {model_id}")
                except Exception as e:
                    print(f"Error stopping container for {model_id}: {e}")

        # Save the performance data
        data_file = (
            self.raw_data_dir
            / f"sequential_all_containers_{self.timestamp}.json"
        )
        with open(data_file, "w") as f:
            json.dump(performance_data, f, indent=2)

        # Generate visualizations
        viz_paths = self.visualizer.create_visualizations(
            performance_data,
            prefix="sequential_all_containers",
        )

        # Generate summary report
        report_file = (
            self.raw_data_dir
            / f"sequential_all_containers_{self.timestamp}_report.txt"
        )
        report = self.visualizer.generate_summary_report(
            performance_data, output_file=str(report_file)
        )

        # Create a summary file with links to all individual test results
        summary_file = (
            self.results_dir
            / f"sequential_all_containers_summary_{self.timestamp}.json"
        )
        with open(summary_file, "w") as f:
            json.dump(
                {
                    "timestamp": self.timestamp,
                    "mode": "sequential_all_containers",
                    "models_tested": models,
                    "active_models": active_models,
                    "model_results": all_model_data,
                    "data_file": str(data_file),
                    "report_file": str(report_file),
                    "visualizations": viz_paths,
                },
                f,
                indent=2,
            )

        print(f"\nSequential all containers testing completed!")
        print(f"Performance data saved to {data_file}")
        print(f"Summary saved to {summary_file}")

        return {
            "summary_file": str(summary_file),
            "data_file": str(data_file),
            "report": report,
            "visualizations": viz_paths,
            "model_results": all_model_data,
        }

    def _start_monitoring(self, data_list, interval=1.0):
        """Start the performance monitoring thread"""
        stop_event = threading.Event()

        def monitor_loop():
            while not stop_event.is_set():
                snapshot = self.monitor.capture_performance_snapshot()
                data_list.append(snapshot)
                time.sleep(interval)

        monitor_thread = threading.Thread(target=monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()

        return (monitor_thread, stop_event)

    def _stop_monitoring(self, monitor_thread_data):
        """Stop the performance monitoring thread"""
        monitor_thread, stop_event = monitor_thread_data
        stop_event.set()
        monitor_thread.join(timeout=2.0)


def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description="Run performance tests on Docker containers for LLM models"
    )

    parser.add_argument(
        "--mode",
        "-m",
        choices=["sequential", "sequential_all_containers"],
        default="sequential_all_containers",
        help="Test mode: sequential (one container at a time) or sequential_all_containers (start all, prompt sequentially, stop all)",
    )

    parser.add_argument(
        "--models",
        nargs="+",
        help="Space-separated list of model IDs to test",
        default=[
            "mistral:7b-instruct-v0.3-q3_K_M",
            "deepseek-coder:6.7b-instruct-q3_K_M",
            "qwen2.5-coder:3b-instruct-q8_0",
            "gemma3:4b-it-q4_K_M",
            "phi4-mini:3.8b-q4_K_M",
        ],
    )

    parser.add_argument(
        "--prompt-file",
        "-p",
        default=PROMPT_FILE,
        help="Path to a file containing the prompt to send",
    )

    parser.add_argument(
        "--output-dir", "-o", help="Directory to save test results"
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit",
    )

    args = parser.parse_args()

    # Create necessary configuration files if they don't exist
    allowed_models = create_or_load_allowed_models_file()

    # Just list models and exit if requested
    if args.list_models:
        print("\nAvailable models for testing:")
        print("-" * 60)
        for model in allowed_models:
            print(f"{model['id']:<30} - {model['name']}")
        print("-" * 60)
        print("Use these IDs with the --models parameter")
        return

    # Determine which models to test
    if args.models:
        models_to_test = args.models
    else:
        # Default to testing 2 models
        available_models = [model["id"] for model in allowed_models]
        models_to_test = available_models[: min(2, len(available_models))]

    # Load the prompt
    prompt = load_prompt(args.prompt_file)

    # Create the output directory
    output_dir = args.output_dir or RESULTS_DIR
    os.makedirs(output_dir, exist_ok=True)

    # Run the requested test
    tester = PerformanceTest(output_dir=output_dir)

    if args.mode == "sequential":
        tester.run_sequential_test(models_to_test, prompt)
    else:  # sequential_all_containers
        tester.run_sequential_all_containers_test(models_to_test, prompt)


if __name__ == "__main__":
    main()
