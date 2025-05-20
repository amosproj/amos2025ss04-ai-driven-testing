#!/usr/bin/env python3
"""Sequential Docker container runner.

This module provides functionality to run multiple Docker containers in sequence,
with controlled execution flow, input/output handling, and automatic cleanup.
It supports continuous execution with user interrupt capabilities.
"""

import subprocess
import time
import sys
import logging
import uuid
import threading
import atexit

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("docker_runner.log"),
    ],
)

# List of Docker containers to run sequentially
# Format: [container_name, input_data]
CONTAINERS = [
    ["nginx:latest", "Hello from container 1"],
    ["alpine:latest", "Hello from container 2"],
    ["ubuntu:latest", "Hello from container 3"],
]

# Global variable to control the main loop
running = True


def ensure_no_leftover_containers():
    """Check and remove any leftover containers from previous runs."""
    try:
        # Find containers with our naming pattern
        cmd = [
            "docker",
            "ps",
            "-a",
            "--filter",
            "name=sequential-runner-",
            "--format",
            "{{.ID}}",
        ]
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True
        )
        container_ids = result.stdout.strip().split("\n")

        # Remove any found containers
        for container_id in container_ids:
            if container_id:
                logging.warning(
                    f"Found leftover container {container_id}, removing it"
                )
                subprocess.run(
                    ["docker", "rm", "-f", container_id],
                    check=True,
                    capture_output=True,
                )
    except Exception as e:
        logging.error(f"Error cleaning up leftover containers: {str(e)}")


def run_container(container_name, input_data):
    """Start a container, provide input, get output, and stop the container.

    Args:
        container_name (str): Name/image of the Docker container
        input_data (str): Input to provide to the container

    Returns:
        str: Output from the container or error message
    """
    # Generate a unique container name to track it
    unique_container_name = f"sequential-runner-{uuid.uuid4().hex[:8]}"

    try:
        # Pull the image if not already available
        logging.info(f"Pulling image: {container_name}")
        subprocess.run(
            ["docker", "pull", container_name], check=True, capture_output=True
        )

        # Start the container with a command that will process input
        # Using echo as a simple example - replace with appropriate command for actual use case
        logging.info(
            f"Starting container: {container_name} as {unique_container_name}"
        )
        container_process = subprocess.run(
            [
                "docker",
                "run",
                "--name",
                unique_container_name,
                "--rm",
                "-i",
                container_name,
                "sh",
                "-c",
                "cat && echo 'Processed input'",
            ],
            input=input_data.encode(),
            capture_output=True,
            check=True,
        )

        output = container_process.stdout.decode().strip()
        logging.info(f"Container {container_name} output: {output}")

        # Verify the container is gone
        verify_cmd = [
            "docker",
            "ps",
            "-a",
            "--filter",
            f"name={unique_container_name}",
            "--format",
            "{{.ID}}",
        ]
        verify_result = subprocess.run(
            verify_cmd, check=True, capture_output=True, text=True
        )
        if verify_result.stdout.strip():
            # Container still exists, force remove it
            container_id = verify_result.stdout.strip()
            logging.warning(
                f"Container {unique_container_name} still running, force removing"
            )
            subprocess.run(
                ["docker", "rm", "-f", container_id],
                check=True,
                capture_output=True,
            )

        return output

    except subprocess.CalledProcessError as e:
        error_msg = f"Error with container {container_name}: {e.stderr.decode() if e.stderr else str(e)}"
        logging.error(error_msg)

        # Try to clean up the container if it's still there
        try:
            verify_cmd = [
                "docker",
                "ps",
                "-a",
                "--filter",
                f"name={unique_container_name}",
                "--format",
                "{{.ID}}",
            ]
            verify_result = subprocess.run(
                verify_cmd, check=True, capture_output=True, text=True
            )
            if verify_result.stdout.strip():
                container_id = verify_result.stdout.strip()
                logging.warning(
                    f"Removing failed container {unique_container_name}"
                )
                subprocess.run(
                    ["docker", "rm", "-f", container_id],
                    check=True,
                    capture_output=True,
                )
        except Exception as cleanup_error:
            logging.error(
                f"Error during container cleanup: {str(cleanup_error)}"
            )

        return error_msg
    except Exception as e:
        error_msg = (
            f"Unexpected error with container {container_name}: {str(e)}"
        )
        logging.error(error_msg)

        # Try to clean up the container if it's still there
        try:
            verify_cmd = [
                "docker",
                "ps",
                "-a",
                "--filter",
                f"name={unique_container_name}",
                "--format",
                "{{.ID}}",
            ]
            verify_result = subprocess.run(
                verify_cmd, check=True, capture_output=True, text=True
            )
            if verify_result.stdout.strip():
                container_id = verify_result.stdout.strip()
                logging.warning(
                    f"Removing failed container {unique_container_name}"
                )
                subprocess.run(
                    ["docker", "rm", "-f", container_id],
                    check=True,
                    capture_output=True,
                )
        except Exception as cleanup_error:
            logging.error(
                f"Error during container cleanup: {str(cleanup_error)}"
            )

        return error_msg


def run_container_sequence():
    """Run containers sequentially and return execution status."""
    results = []

    logging.info("Starting sequential container execution")

    # Check if Docker is available
    try:
        subprocess.run(
            ["docker", "--version"], check=True, capture_output=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.error(
            "Docker is not available. Please install Docker and ensure it's running."
        )
        return False

    # Ensure no leftover containers from previous runs
    ensure_no_leftover_containers()

    # Run each container sequentially
    for i, (container, input_data) in enumerate(CONTAINERS):
        # Check if we should still be running
        if not running:
            logging.info("Sequence terminated by user")
            break

        logging.info(
            f"Processing container {i + 1}/{len(CONTAINERS)}: {container}"
        )
        result = run_container(container, input_data)
        results.append((container, result))

    # Final verification that no containers are running from our script
    ensure_no_leftover_containers()

    # Verify that no containers from our script are running
    try:
        cmd = [
            "docker",
            "ps",
            "--filter",
            "name=sequential-runner-",
            "--format",
            "{{.ID}}",
        ]
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True
        )
        if result.stdout.strip():
            logging.error(
                f"WARNING: There are still containers running: {result.stdout.strip()}"
            )
        else:
            logging.info(
                "Verified no containers are running - cleanup successful"
            )
    except Exception as e:
        logging.error(f"Error during final verification: {str(e)}")

    # Print summary of results
    logging.info("\n----- Results Summary -----")
    for container, result in results:
        logging.info(f"Container: {container}")
        logging.info(f"Result: {result}")
        logging.info("--------------------------")

    logging.info("Container sequence completed successfully")
    return True


def input_listener():
    """Listen for user input to quit the program."""
    global running
    print("Press 'q' and Enter to quit at any time...")

    while running:
        try:
            if input().lower().strip() == "q":
                print("Quitting after current container finishes...")
                logging.info("User requested termination")
                running = False
                break
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+C or other interrupts
            running = False
            break


def cleanup():
    """Ensure cleanup of resources on program exit."""
    logging.info("Performing final cleanup...")
    ensure_no_leftover_containers()
    logging.info("Cleanup completed")


def main():
    """Execute the main program loop for container sequencing."""
    global running

    # Register cleanup function to run at program exit
    atexit.register(cleanup)

    # Start input listener thread
    listener_thread = threading.Thread(target=input_listener)
    listener_thread.daemon = True
    listener_thread.start()

    logging.info("Container runner started in continuous mode")
    print(
        "Container runner started. Containers will run in sequence continuously."
    )
    print("Press 'q' and Enter to quit.")

    try:
        # Keep running until user quits
        run_count = 0
        while running:
            run_count += 1
            logging.info(f"=== Starting run #{run_count} ===")
            success = run_container_sequence()

            if not success:
                logging.error("Container sequence failed - stopping")
                running = False
                break

            # If we're still running, wait a bit before starting the next sequence
            if running:
                logging.info("Waiting 10 seconds before next sequence...")
                # Use small sleep increments to check running status
                for _ in range(10):
                    if not running:
                        break
                    time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Interrupted by user (Ctrl+C)")
    finally:
        running = False
        logging.info("Waiting for threads to complete...")
        listener_thread.join(timeout=2.0)
        logging.info("Exiting")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Unhandled exception in main process: {str(e)}")
        # Final cleanup attempt if something went wrong
        ensure_no_leftover_containers()
        sys.exit(1)
