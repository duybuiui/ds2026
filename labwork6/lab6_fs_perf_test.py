import os
import time
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor

class FileSystemStressTest:
    def __init__(self, target_dir, num_threads=4):
        self.target_dir = target_dir
        self.small_dir = os.path.join(target_dir, "small_io_test")
        self.large_dir = os.path.join(target_dir, "throughput_test")
        self.num_threads = num_threads
        self._prepare_environment()

    def _prepare_environment(self):
        if os.path.exists(self.small_dir):
            shutil.rmtree(self.small_dir)
        os.makedirs(self.small_dir)
        
        if not os.path.exists(self.large_dir):
            os.makedirs(self.large_dir)

    def _small_file_worker(self, file_id):
        filepath = os.path.join(self.small_dir, f"file_{file_id}.txt")
        with open(filepath, "w") as f:
            f.write("data" * 10)
        with open(filepath, "r") as f:
            _ = f.read()

    def measure_small_io(self, total_files=2000):
        print(f"[TEST] Small IO: Processing {total_files} files using {self.num_threads} threads...")
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            executor.map(self._small_file_worker, range(total_files))
            
        duration = time.time() - start
        total_ops = total_files * 2
        ops_per_sec = total_ops / duration
        print(f"[RESULT] Small IO Speed: {ops_per_sec:.2f} accesses/sec")
        return ops_per_sec

    def measure_throughput(self, file_size_mb=1024):
        print(f"[TEST] Throughput: Reading {file_size_mb} MB file...")
        filename = os.path.join(self.large_dir, "big_data.bin")
        
        with open(filename, "wb") as f:
            f.write(os.urandom(file_size_mb * 1024 * 1024))
        
        os.system("sync")
        
        start = time.time()
        with open(filename, "rb") as f:
            while f.read(1024 * 1024):
                pass
        duration = time.time() - start
        
        speed = file_size_mb / duration
        print(f"[RESULT] Read Throughput: {speed:.2f} MB/s")
        return speed

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fs_perf_test.py <mount_point>")
        sys.exit(1)
        
    mount_point = sys.argv[1]
    tester = FileSystemStressTest(mount_point)
    tester.measure_small_io()
    tester.measure_throughput()