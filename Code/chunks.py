import os
import struct

def parse_jpeg_chunks(file_path):
    """
    Parses chunks (markers) in a JPEG file.
    Returns a list of tuples: (marker, offset, length).
    """
    chunks = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            offset = 0

            # JPEG files start with SOI marker (0xFFD8)
            if data[:2] != b'\xFF\xD8':
                return f"{file_path} is not a valid JPEG file."

            offset += 2
            while offset < len(data):
                if data[offset] == 0xFF:
                    marker = data[offset:offset+2]
                    if marker == b'\xFF\xD9':  # EOI (End of Image)
                        chunks.append((marker, offset, 0))
                        break
                    length = struct.unpack(">H", data[offset+2:offset+4])[0]
                    chunks.append((marker, offset, length))
                    offset += length + 2
                else:
                    break
    except Exception as e:
        return f"Error parsing {file_path}: {e}"
    return chunks

def compare_jpeg_files(file_paths, output_file="output1.txt"):
    """
    Compares JPEG files by analyzing their chunks and exports the results.
    """
    results = []
    all_chunks = {}

    for file_path in file_paths:
        chunks = parse_jpeg_chunks(file_path)
        if isinstance(chunks, str):  # Error message
            results.append(chunks)
        else:
            all_chunks[file_path] = chunks
            results.append(f"File: {file_path}")
            results.append("Chunks:")
            for marker, offset, length in chunks:
                results.append(f"  Marker: {marker} | Offset: {offset} | Length: {length}")
            results.append("-" * 60)

    # Find common chunks across files
    common_chunks = {}
    for file1, chunks1 in all_chunks.items():
        for file2, chunks2 in all_chunks.items():
            if file1 == file2:
                continue
            for chunk1 in chunks1:
                if chunk1 in chunks2:
                    common_chunks.setdefault((file1, file2), []).append(chunk1)

    results.append("\nCommon Chunks Across Files:")
    if not common_chunks:
        results.append("No common chunks found.")
    else:
        for (file1, file2), chunks in common_chunks.items():
            results.append(f"Common Chunks between {file1} and {file2}:")
            for marker, offset, length in chunks:
                results.append(f"  Marker: {marker} | Offset in {file1}: {offset} | Length: {length}")
            results.append("-" * 60)

    # Write results to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(results))
    print(f"Comparison results written to {output_file}")

# Main Execution
if __name__ == "__main__":
    # Replace with the directory containing JPEG files
    directory = "./jpeg_files"
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(".jpg")]

    if not file_paths:
        print("No JPEG files found in the directory.")
    else:
        print(f"Comparing {len(file_paths)} JPEG files...")
        compare_jpeg_files(file_paths)
