import binascii

def read_file_as_hex(file_path):
    """
    Reads the content of a file and converts it to a hexadecimal string.
    """
    with open(file_path, "rb") as f:
        return f.read()

def find_common_chunks(file1, file2, chunk_size=8):
    """
    Finds common chunks between two binary files and their offsets.
    Args:
        file1: Path to the first file.
        file2: Path to the second file.
        chunk_size: The size of chunks to compare (in bytes).
    Returns:
        A list of tuples: (offset_in_file1, offset_in_file2, chunk_data)
    """
    data1 = read_file_as_hex(file1)
    data2 = read_file_as_hex(file2)
    common_chunks = []

    for offset1 in range(len(data1) - chunk_size + 1):
        chunk = data1[offset1 : offset1 + chunk_size]
        offset2 = data2.find(chunk)
        if offset2 != -1:
            common_chunks.append((offset1, offset2, chunk))

    return common_chunks

def compare_files(file1, file2):
    """
    Compares two files for common hex chunks and prints the results.
    """
    print(f"Comparing {file1} and {file2}...")
    chunk_size = 8  # Adjust for the desired chunk size (in bytes)

    # Find common chunks
    common_chunks = find_common_chunks(file1, file2, chunk_size)

    if not common_chunks:
        print("No common chunks found.")
    else:
        print(f"Found {len(common_chunks)} common chunk(s):\n")
        for offset1, offset2, chunk in common_chunks:
            print(f"Chunk: {binascii.hexlify(chunk)}")
            print(f" - Offset in {file1}: {offset1} bytes (from start)")
            print(f" - Offset in {file2}: {offset2} bytes (from start)")
            print(f" - Distance from header in {file1}: {offset1 - 64 if offset1 > 64 else 'In Header'} bytes")
            print(f" - Distance from header in {file2}: {offset2 - 64 if offset2 > 64 else 'In Header'} bytes\n")

# Main Execution
if __name__ == "__main__":
    # Replace with your image file paths
    file1 = "Geminii.jpg"
    file2 = "Geminiv.jpg"

    compare_files(file1, file2)
