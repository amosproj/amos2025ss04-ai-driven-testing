import threading
import random
import time
import requests
import json
from pathlib import Path

class DataProcessor:
    def __init__(self, urls, output_file):
        self.urls = urls
        self.output_file = Path(output_file)
        self.results = []
        self.lock = threading.Lock()

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
        return {}

    def process_data(self, data):
        # Simulate random processing delay and random result selection
        time.sleep(random.uniform(0.1, 0.5))
        return {k: v for k, v in data.items() if random.choice([True, False])}

    def worker(self, url):
        raw = self.fetch_data(url)
        processed = self.process_data(raw)
        with self.lock:
            self.results.append(processed)

    def run(self):
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
        self.output_file.write_text(json.dumps(self.results, indent=2))


if __name__ == "__main__":
    processor = DataProcessor(
        urls=[
            "https://jsonplaceholder.typicode.com/todos/1",
            "https://jsonplaceholder.typicode.com/todos/2"
        ],
        output_file="output.json"
    )
    processor.run()
