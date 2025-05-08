"""Threaded data processor for fetching and processing JSON data from URLs.

This module provides a DataProcessor class that uses threading to concurrently
fetch JSON data from multiple URLs, process the data, and save the results to
a file. It demonstrates concurrent programming concepts using Python's threading
module.
"""

import json
import random
import threading
import time
from pathlib import Path

import requests


class DataProcessor:
    """A threaded data processing system for handling multiple URLs concurrently.

    This class fetches data from multiple URLs in parallel using threads,
    processes the data, and saves the combined results to a JSON file.
    It demonstrates thread-safe operations using locks.
    """

    def __init__(self, urls, output_file):
        """Initialize the DataProcessor with URLs and an output file path.

        Args:
            urls: List of URLs to fetch data from
            output_file: Path where the processed results will be saved
        """
        self.urls = urls
        self.output_file = Path(output_file)
        self.results = []
        self.lock = threading.Lock()

    def fetch_data(self, url):
        """Fetch JSON data from a URL.

        Makes an HTTP GET request to the specified URL and returns the
        JSON response, or an empty dict if the request fails.

        Args:
            url: The URL to fetch data from

        Returns:
            dict: The JSON data from the response, or an empty dict on failure
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
        return {}

    def process_data(self, data):
        """Process the data with random selection and artificial delay.

        Simulates data processing by randomly selecting key-value pairs
        from the input data and introducing a random delay.

        Args:
            data: The data dictionary to process

        Returns:
            dict: A dictionary containing randomly selected items from the input
        """
        # Simulate random processing delay and random result selection
        time.sleep(random.uniform(0.1, 0.5))
        return {k: v for k, v in data.items() if random.choice([True, False])}

    def worker(self, url):
        """Worker function for thread execution.

        Fetches data from a URL, processes it, and adds the results to
        the shared results list in a thread-safe manner.

        Args:
            url: The URL to process
        """
        raw = self.fetch_data(url)
        processed = self.process_data(raw)
        with self.lock:
            self.results.append(processed)

    def run(self):
        """Run the data processing operation with multiple threads.

        Creates and starts a thread for each URL, waits for all threads
        to complete, then saves the combined results.
        """
        threads = [
            threading.Thread(target=self.worker, args=(url,))
            for url in self.urls
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.save_results()

    def save_results(self):
        """Save the processed results to the output file in JSON format.

        Writes the contents of the results list to the specified output
        file with pretty formatting (indentation).
        """
        self.output_file.write_text(json.dumps(self.results, indent=2))


if __name__ == "__main__":
    processor = DataProcessor(
        urls=[
            "https://jsonplaceholder.typicode.com/todos/1",
            "https://jsonplaceholder.typicode.com/todos/2",
        ],
        output_file="output.json",
    )
    processor.run()
