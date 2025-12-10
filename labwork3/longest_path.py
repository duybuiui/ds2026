import sys
def mapper(data_chunk):
    """
    Mapper receives a list of file paths (lines).
    Task: Find the longest path within this specific chunk.
    Output: A tuple (Key, Value) -> ('MAX', local_longest_path)
    """
    local_max_len = 0
    local_max_path = ""

    for path in data_chunk:
        path = path.strip()
        current_len = len(path)
        if current_len > local_max_len:
            local_max_len = current_len
            local_max_path = path

    return ("MAX", local_max_path)
def reducer(mapped_results):
    """
    Reducer receives a list of results from all Mappers.
    Task: Compare the longest paths found by mappers to find the global longest path.
    Output: The single longest path string.
    """
    global_max_len = 0
    global_max_path = ""

    for key, path in mapped_results:
        current_len = len(path)
        if current_len > global_max_len:
            global_max_len = current_len
            global_max_path = path
            
    return global_max_path
def main():
    input_file = 'input_paths.txt'
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
    except FileNotFoundError:
        print(f"File '{input_file}' not found. Please run the 'find' command first to generate input.")
        return

    num_mappers = 4
    if len(all_lines) == 0:
        print("Input file is empty.")
        return

    chunk_size = len(all_lines) // num_mappers + 1
    chunks = [all_lines[i:i + chunk_size] for i in range(0, len(all_lines), chunk_size)]

    print(f"Total lines: {len(all_lines)}")
    print(f"Split into {len(chunks)} chunks for Mappers.")
    map_outputs = []
    for i, chunk in enumerate(chunks):
        if not chunk: continue
        result = mapper(chunk)
        map_outputs.append(result)

    final_result = reducer(map_outputs)
    print("-" * 30)
    print("FINAL RESULT - LONGEST PATH:")
    print(f"Length: {len(final_result)}")
    print(f"Path: {final_result}")

if __name__ == "__main__":
    main()