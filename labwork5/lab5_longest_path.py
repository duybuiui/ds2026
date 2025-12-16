import multiprocessing
import os
import sys

def map_worker(path_chunk):
    if not path_chunk:
        return None
    local_longest = max(path_chunk, key=len)
    return ("MAX", local_longest)

def reduce_worker(item):
    key, paths = item
    if not paths:
        return None
    global_longest = max(paths, key=len)
    return (key, global_longest)

class LongestPathMapReduce:
    def __init__(self, input_file, num_workers=4):
        self.input_file = input_file
        self.num_workers = num_workers

    def generate_dummy_data(self):
        paths = [
            "/usr/bin",
            "/usr/local/bin/python3",
            "/var/log/system.log",
            "/home/user/documents/projects/mapreduce/lab5/longest_path.py",
            "/tmp",
            "/etc/hosts",
            "/opt/google/chrome/chrome",
            "/very/long/path/created/just/for/testing/the/algorithm/to/see/if/it/catches/this/specific/string"
        ]
        with open(self.input_file, 'w') as f:
            for p in paths:
                f.write(p + '\n')

    def read_input(self):
        if not os.path.exists(self.input_file):
            self.generate_dummy_data()
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines

    def split_data(self, data):
        chunk_size = len(data) // self.num_workers + 1
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    def run(self):
        print(f"--- Starting Longest Path MapReduce (Workers: {self.num_workers}) ---")

        data = self.read_input()
        chunks = self.split_data(data)
        print(f"[Master] Input loaded. Total paths: {len(data)}")

        print("[Master] Map Phase: Finding local longest paths...")
        with multiprocessing.Pool(processes=self.num_workers) as pool:
            mapped_results = pool.map(map_worker, chunks)
        
        valid_results = [res for res in mapped_results if res is not None]

        print("[Master] Shuffle Phase: Aggregating local maximums...")
        shuffled_data = []
        for key, value in valid_results:
            shuffled_data.append(value)

        print("[Master] Reduce Phase: Finding global longest path...")
        final_key, final_value = reduce_worker(("MAX", shuffled_data))

        print("-" * 40)
        print(f"RESULT: LONGEST PATH FOUND")
        print("-" * 40)
        print(f"Length: {len(final_value)}")
        print(f"Path  : {final_value}")

if __name__ == "__main__":
    job = LongestPathMapReduce("file_paths.txt", num_workers=4)
    job.run()