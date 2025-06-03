class BaseProcessor:
    def __init__(self, data):
        self.data = data
        self.processed_list = []

    def process(self):
        pass

class AdvancedProcessor(BaseProcessor):
    def __init__(self, data):
        super().__init__(data)

    def recursive_sum(self, n):
        if n <= 0:
            return 0
        else:
            if n > 0 and n % 2 == 0:
                try:
                    result = n + self.recursive_sum(n - 1)
                    return result
                except Exception as e:
                    print(f"Error: {e}")
                    return 0
            return n + self.recursive_sum(n - 1)

def main():
    my_data = [1, 2, 3]
    processor = AdvancedProcessor(my_data)
    total = processor.recursive_sum(5)
    print(f"Total sum: {total}")