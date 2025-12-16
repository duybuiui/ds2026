import sys
import re
from collections import defaultdict

class WordCountMapReduce:
    def __init__(self, input_filename):
        self.input_filename = input_filename
        self.data_splits = []

    def load_and_split_data(self, num_chunks=3):
        """
        Reads the file and simulates splitting data for workers.
        """
        try:
            with open(self.input_filename, 'r', encoding='utf-8') as f:
                content = f.read()
            lines = content.splitlines()
            if not lines:
                print("[System] Input file is empty.")
                return False
            chunk_size = (len(lines) // num_chunks) + 1
            self.data_splits = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
            print(f"[System] Data split into {len(self.data_splits)} chunks.")
            return True
        except FileNotFoundError:
            print(f"[Error] File '{self.input_filename}' not found.")
            return False

    def mapper(self, text_chunk):
        """
        Mapper: Processes a list of lines.
        Output: List of (word, 1)
        """
        intermediate = []
        for line in text_chunk:
            clean_line = re.sub(r'[^\w\s]', '', line).lower()
            words = clean_line.split()
            for word in words:
                intermediate.append((word, 1))
        return intermediate

    def reducer(self, key, values):
        """
        Reducer: Sums up the counts for a specific word (key).
        Output: (word, total_count)
        """
        return (key, sum(values))

    def shuffle_and_sort(self, mapped_results):
        """
        Simulates the Shuffle phase: Grouping values by Key.
        """
        grouped_data = defaultdict(list)
        for result in mapped_results:
            for key, value in result:
                grouped_data[key].append(value)
        return grouped_data

    def run(self):
        if not self.load_and_split_data():
            return
        print("[System] Starting Map phase...")
        mapped_results = []
        for i, chunk in enumerate(self.data_splits):
            res = self.mapper(chunk)
            mapped_results.append(res)

        print("[System] Starting Shuffle & Sort phase...")
        grouped_data = self.shuffle_and_sort(mapped_results)

        print("[System] Starting Reduce phase...")
        final_output = {}
        for word, counts in grouped_data.items():
            _, total = self.reducer(word, counts)
            final_output[word] = total

        print("="*40)
        print(f"{'WORD':<20} | {'COUNT':<10}")
        print("="*40)
        sorted_results = sorted(final_output.items(), key=lambda x: x[1], reverse=True)
        for word, count in sorted_results:
            print(f"{word:<20} | {count:<10}")

if __name__ == "__main__":
    import os
    if not os.path.exists("input.txt"):
        with open("input.txt", "w") as f:
            f.write("Hello world\nHello MapReduce\nMapReduce is cool\nDistributed systems are cool")
    
    job = WordCountMapReduce("input.txt")
    job.run()