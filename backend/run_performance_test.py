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

# Check if module exists before importing
from llm_manager import LLMManager
from performance_monitor import PerformanceMonitor
from performance_visualization import PerformanceVisualizer

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEST_DURATION = 6000  # seconds
RESULTS_DIR = os.path.join(SCRIPT_DIR, "performance_results")
PROMPT_FILE = os.path.join(SCRIPT_DIR, "prompt.txt")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "allowed_models.json")

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
        default_models = [
            {"id": "mistral:7b-instruct-v0.3-q3_K_M", "name": "Mistral 7B Instruct", "description": "Good general purpose language model"},
            {"id": "deepseek-coder:6.7b-instruct-q3_K_M", "name": "DeepSeek Coder 6.7B", "description": "Specialized for code generation"},
            {"id": "qwen2.5-coder:3b-instruct-q8_0", "name": "Qwen2 Coder 3B", "description": "Smaller code generation model"},
            {"id": "gemma3:4b-it-q4_K_M", "name": "Gemma3 4B", "description": "Google's general purpose model"},
            {"id": "phi4-mini:3.8b-q4_K_M", "name": "Phi-4 Mini", "description": "Microsoft's small but capable model"}
        ]
        
        config = {"models": default_models}
        
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        print(f"Created default allowed_models.json at {CONFIG_FILE}")
        return default_models
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
        self.monitor = PerformanceMonitor(output_dir=output_dir or os.path.join(RESULTS_DIR, "raw_data"))
        self.visualizer = PerformanceVisualizer(output_dir=output_dir or RESULTS_DIR)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = Path(output_dir or RESULTS_DIR)
        self.results_dir.mkdir(exist_ok=True, parents=True)
        
        # Ensure raw_data subdirectory exists
        raw_data_dir = self.results_dir / "raw_data"
        raw_data_dir.mkdir(exist_ok=True, parents=True)
    
    def run_sequential_test(self, models, prompt, test_duration=60):
        """
        Run models sequentially and measure performance
        
        Args:
            models: List of model IDs to test
            prompt: Prompt to send to each model
            test_duration: Duration to run each model in seconds
            
        Returns:
            Dictionary with test results
        """
        print(f"\nRunning sequential test with {len(models)} models")
        print(f"Each model will run for approximately {test_duration} seconds\n")
        
        all_model_data = []
        
        for model_id in models:
            print(f"\n{'='*50}")
            print(f"Testing model: {model_id}")
            print(f"{'='*50}")
            
            # Start collecting performance data
            performance_data = []
            monitor_thread = self._start_monitoring(performance_data, interval=1.0)
            
            try:
                # Start the container
                self.llm_manager.start_model_container(model_id)
                print(f"Started container for {model_id}")
                
                # Send the prompt
                start_time = time.time()
                print(f"Sending prompt to {model_id}...")
                
                # Use a custom output file for this test
                output_file = f"sequential_test_{model_id.replace(':', '_')}_{self.timestamp}.md"
                self.llm_manager.send_prompt(model_id, prompt, output_file=output_file)
                
                # Wait for the desired duration if needed
                elapsed = time.time() - start_time
                if elapsed < test_duration:
                    remaining = test_duration - elapsed
                    print(f"Waiting {remaining:.1f} seconds to complete the test duration...")
                    time.sleep(remaining)
                
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
            model_data_file = self.results_dir / "raw_data" / f"sequential_{model_id.replace(':', '_')}_{self.timestamp}.json"
            with open(model_data_file, "w") as f:
                json.dump(performance_data, f, indent=2)
            
            # Generate visualizations for this model
            viz_paths = self.visualizer.create_visualizations(performance_data)
            
            # Generate summary report
            report = self.visualizer.generate_summary_report(
                performance_data, 
                output_file=str(self.results_dir / "raw_data" / f"sequential_{model_id.replace(':', '_')}_{self.timestamp}_report.txt")
            )
            
            print(f"\nTest completed for {model_id}")
            print(f"Performance data saved to {model_data_file}")
            
            # Store data for overall summary
            all_model_data.append({
                "model_id": model_id,
                "data_file": str(model_data_file),
                "visualizations": viz_paths,
                "report": report
            })
        
        # Create a summary file with links to all individual test results
        summary_file = self.results_dir / f"sequential_test_summary_{self.timestamp}.json"
        with open(summary_file, "w") as f:
            json.dump({
                "timestamp": self.timestamp,
                "mode": "sequential",
                "models_tested": models,
                "test_duration": test_duration,
                "results": all_model_data
            }, f, indent=2)
        
        print(f"\nSequential testing completed!")
        print(f"Summary saved to {summary_file}")
        
        return {
            "summary_file": str(summary_file),
            "model_results": all_model_data
        }
    
    def run_parallel_test(self, models, prompt, test_duration=60000):
        """
        Run models in parallel and measure performance
        
        Args:
            models: List of model IDs to test in parallel
            prompt: Prompt to send to each model
            test_duration: How long to run the test in seconds
            
        Returns:
            Dictionary with test results
        """
        print(f"\nRunning parallel test with {len(models)} models simultaneously")
        print(f"Test will run for approximately {test_duration} seconds\n")
        
        # Start collecting performance data
        performance_data = []
        monitor_thread = self._start_monitoring(performance_data, interval=1.0)
        
        try:
            # Start all containers
            for model_id in models:
                try:
                    self.llm_manager.start_model_container(model_id)
                    print(f"Started container for {model_id}")
                except Exception as e:
                    print(f"Error starting container for {model_id}: {e}")
            
            # Create threads for sending prompts to each model
            prompt_threads = []
            for model_id in models:
                output_file = f"parallel_test_{model_id.replace(':', '_')}_{self.timestamp}.md"
                thread = threading.Thread(
                    target=self._send_prompt_thread,
                    args=(model_id, prompt, output_file)
                )
                prompt_threads.append(thread)
            
            # Start all prompt threads
            for thread in prompt_threads:
                thread.start()
            
            # If any threads are still running after test_duration, we'll let them continue
            # but we'll stop monitoring at the desired time
            start_time = time.time()
            while time.time() - start_time < test_duration:
                # Check if all threads have completed
                if not any(thread.is_alive() for thread in prompt_threads):
                    print("All models have completed processing")
                    break
                time.sleep(1)
            
            # Wait for a short additional time to capture post-processing metrics
            time.sleep(5)
            
        finally:
            # Stop monitoring
            self._stop_monitoring(monitor_thread)
            
            # Stop all containers
            for model_id in models:
                try:
                    self.llm_manager.stop_model_container(model_id)
                    print(f"Stopped container for {model_id}")
                except Exception as e:
                    print(f"Error stopping container for {model_id}: {e}")
        
        # Save the performance data
        data_file = self.results_dir / "raw_data" / f"parallel_test_{self.timestamp}.json"
        with open(data_file, "w") as f:
            json.dump(performance_data, f, indent=2)
        
        # Generate visualizations
        viz_paths = self.visualizer.create_visualizations(performance_data)
        
        # Generate summary report
        report_file = self.results_dir / "raw_data" / f"parallel_test_{self.timestamp}_report.txt"
        report = self.visualizer.generate_summary_report(performance_data, output_file=str(report_file))
        
        # Create a summary file
        summary_file = self.results_dir / f"parallel_test_summary_{self.timestamp}.json"
        with open(summary_file, "w") as f:
            json.dump({
                "timestamp": self.timestamp,
                "mode": "parallel",
                "models_tested": models,
                "test_duration": test_duration,
                "data_file": str(data_file),
                "report_file": str(report_file),
                "visualizations": viz_paths
            }, f, indent=2)
        
        print(f"\nParallel testing completed!")
        print(f"Performance data saved to {data_file}")
        print(f"Summary saved to {summary_file}")
        
        return {
            "summary_file": str(summary_file),
            "data_file": str(data_file),
            "report": report,
            "visualizations": viz_paths
        }
    
    def run_benchmark_test(self, models, prompt, test_duration=60):
        """
        Run comprehensive benchmarks including both sequential and parallel tests
        
        Args:
            models: List of model IDs to test
            prompt: Prompt to send to each model
            test_duration: Duration for each test phase in seconds
            
        Returns:
            Dictionary with test results
        """
        print(f"\nRunning comprehensive benchmark tests")
        print(f"Testing {len(models)} models both sequentially and in parallel")
        print(f"Each test phase will run for approximately {test_duration} seconds\n")
        
        # Run sequential test first to establish baseline
        print("\n==== SEQUENTIAL BENCHMARK PHASE ====")
        sequential_results = self.run_sequential_test(models, prompt, test_duration)
        
        # Run parallel test
        print("\n==== PARALLEL BENCHMARK PHASE ====")
        parallel_results = self.run_parallel_test(models, prompt, test_duration)
        
        # Create benchmark summary
        summary_file = self.results_dir / f"benchmark_summary_{self.timestamp}.json" 
        with open(summary_file, "w") as f:
            json.dump({
                "timestamp": self.timestamp,
                "mode": "benchmark",
                "models_tested": models,
                "test_duration": test_duration,
                "sequential_results": sequential_results,
                "parallel_results": parallel_results,
            }, f, indent=2)
            
        # Create an HTML report with comparisons and analysis
        self._generate_html_report(summary_file)
        
        print(f"\nBenchmark testing completed!")
        print(f"Results saved to {summary_file}")
        
        return {
            "summary_file": str(summary_file),
            "sequential_results": sequential_results,
            "parallel_results": parallel_results
        }
    
    def _send_prompt_thread(self, model_id, prompt, output_file):
        """Thread function to send a prompt to a model"""
        try:
            print(f"Sending prompt to {model_id}...")
            self.llm_manager.send_prompt(model_id, prompt, output_file=output_file)
        except Exception as e:
            print(f"Error sending prompt to {model_id}: {e}")
    
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
    
    def _generate_html_report(self, summary_file):
        """Generate a comprehensive HTML report with visualizations and analysis"""
        # Load the summary data
        with open(summary_file, "r") as f:
            summary = json.load(f)
        
        # Create HTML file
        html_file = self.results_dir / f"benchmark_report_{self.timestamp}.html"
        
        # Basic HTML structure for the report
        html_content = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "    <title>LLM Container Performance Benchmark Report</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }",
            "        h1, h2, h3 { color: #333; }",
            "        .container { max-width: 1200px; margin: 0 auto; }",
            "        .section { margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px; }",
            "        .viz-container { display: flex; flex-wrap: wrap; gap: 20px; }",
            "        .viz-item { flex: 1; min-width: 300px; margin-bottom: 20px; }",
            "        img { max-width: 100%; height: auto; border: 1px solid #ddd; }",
            "        table { border-collapse: collapse; width: 100%; }",
            "        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "        th { background-color: #f2f2f2; }",
            "        .conclusion { background-color: #f9f9f9; padding: 15px; border-radius: 5px; }",
            "    </style>",
            "</head>",
            "<body>",
            "    <div class='container'>",
            f"        <h1>LLM Container Performance Benchmark Report</h1>",
            f"        <p>Test performed on: {datetime.fromtimestamp(summary['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}</p>",
            f"        <p>Models tested: {', '.join(summary['models_tested'])}</p>",
            f"        <p>Test duration per phase: {summary['test_duration']} seconds</p>",
            
            "        <div class='section'>",
            "            <h2>Summary of Findings</h2>",
            "            <p>This benchmark test compares the performance of running LLM models sequentially vs. in parallel.</p>",
            "            <div class='conclusion'>",
            "                <h3>Conclusion</h3>",
            "                <p>Based on the performance metrics collected during this benchmark:</p>",
            "                <ul>"
        ]
        
        # Add analysis of results - parse the reports to get meaningful insights
        sequential_report_path = None
        if 'sequential_results' in summary and 'model_results' in summary['sequential_results']:
            for model_result in summary['sequential_results']['model_results']:
                if 'report' in model_result:
                    sequential_report_path = os.path.join(self.results_dir, "raw_data", 
                                                         f"sequential_{model_result['model_id'].replace(':', '_')}_{self.timestamp}_report.txt")

        parallel_report_path = None
        if 'parallel_results' in summary and 'report_file' in summary['parallel_results']:
            parallel_report_path = summary['parallel_results']['report_file']
        
        # Add basic conclusion based on whether we have reports
        if sequential_report_path and parallel_report_path:
            html_content.append(f"                    <li>The test results provide information on whether running models in parallel or sequentially is more efficient.</li>")
            html_content.append(f"                    <li>See the detailed metrics and visualizations below to determine which configuration best suits your needs.</li>")
            html_content.append(f"                    <li>To determine if containers need to be stopped after use, compare the resource usage patterns between sequential and parallel runs.</li>")
        else:
            html_content.append(f"                    <li>Limited data available to draw definitive conclusions.</li>")
            html_content.append(f"                    <li>Please analyze the raw data and visualizations to determine optimal container management strategy.</li>")
        
        # Complete the HTML structure
        html_content.extend([
            "                </ul>",
            "            </div>",
            "        </div>",
            
            "        <div class='section'>",
            "            <h2>Sequential Test Results</h2>"
        ])
        
        # Add sequential test visualizations 
        if 'sequential_results' in summary and 'model_results' in summary['sequential_results']:
            for model_result in summary['sequential_results']['model_results']:
                html_content.append(f"            <h3>Model: {model_result['model_id']}</h3>")
                html_content.append("            <div class='viz-container'>")
                
                if 'visualizations' in model_result:
                    for viz_type, viz_path in model_result['visualizations'].items():
                        rel_path = os.path.relpath(viz_path, os.path.dirname(html_file))
                        html_content.append(f"                <div class='viz-item'>")
                        html_content.append(f"                    <h4>{viz_type.replace('_', ' ').title()}</h4>")
                        html_content.append(f"                    <img src='{rel_path}' alt='{viz_type} visualization'>")
                        html_content.append(f"                </div>")
                
                html_content.append("            </div>")
        
        # Add parallel test visualizations
        html_content.append("        </div>")
        html_content.append("        <div class='section'>")
        html_content.append("            <h2>Parallel Test Results</h2>")
        
        if 'parallel_results' in summary and 'visualizations' in summary['parallel_results']:
            html_content.append("            <div class='viz-container'>")
            
            for viz_type, viz_path in summary['parallel_results']['visualizations'].items():
                rel_path = os.path.relpath(viz_path, os.path.dirname(html_file))
                html_content.append(f"                <div class='viz-item'>")
                html_content.append(f"                    <h4>{viz_type.replace('_', ' ').title()}</h4>")
                html_content.append(f"                    <img src='{rel_path}' alt='{viz_type} visualization'>")
                html_content.append(f"                </div>")
            
            html_content.append("            </div>")
        
        # Finish HTML
        html_content.extend([
            "        </div>",
            "    </div>",
            "</body>",
            "</html>"
        ])
        
        # Write the HTML file
        with open(html_file, "w") as f:
            f.write("\n".join(html_content))
        
        print(f"Generated HTML report: {html_file}")

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(
        description="Run performance tests on Docker containers for LLM models"
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["sequential", "parallel", "benchmark"],
        default="benchmark",
        help="Test mode: sequential, parallel, or benchmark (both)"
    )
    
    parser.add_argument(
        "--models",
        nargs="+",
        help="Space-separated list of model IDs to test"
    )
    
    parser.add_argument(
        "--prompt-file", "-p",
        help="Path to a file containing the prompt to send"
    )
    
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=DEFAULT_TEST_DURATION,
        help=f"Test duration in seconds (default: {DEFAULT_TEST_DURATION})"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        help="Directory to save test results"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit"
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
        models_to_test = available_models[:min(2, len(available_models))]
    
    # Load the prompt
    prompt = load_prompt(args.prompt_file)
    
    # Create the output directory
    output_dir = args.output_dir or RESULTS_DIR
    os.makedirs(output_dir, exist_ok=True)
    
    # Run the requested test
    tester = PerformanceTest(output_dir=output_dir)
    
    if args.mode == "sequential":
        tester.run_sequential_test(models_to_test, prompt, args.duration)
    elif args.mode == "parallel":
        tester.run_parallel_test(models_to_test, prompt, args.duration)
    else:  # benchmark
        tester.run_benchmark_test(models_to_test, prompt, args.duration)

if __name__ == "__main__":
    main()