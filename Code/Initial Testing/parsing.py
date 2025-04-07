import os
import struct
import binascii

def parse_jpeg_chunks(file_path):
    """Parses chunks (markers) in a JPEG file."""
    chunks = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            offset = 0

            if data[:2] != b'\xFF\xD8':
                return None

            offset += 2
            while offset < len(data):
                if data[offset] == 0xFF:
                    marker = data[offset:offset+2]
                    if marker == b'\xFF\xD9':  # EOI
                        chunks.append((marker, offset, 0, b""))
                        break
                    length = struct.unpack(">H", data[offset+2:offset+4])[0]
                    chunk_data = data[offset+4:offset+4+length-2]
                    chunks.append((marker, offset, length, chunk_data))
                    offset += length + 2
                else:
                    break
    except Exception as e:
        return f"Error parsing {file_path}: {e}"
    return chunks

def parse_webp_chunks(file_path):
    """Parses ALL top-level chunks in a WebP file from start to end, safely."""
    chunks = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()

            if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
                return None

            offset = 12  # Skip RIFF header
            data_length = len(data)

            while offset + 8 <= data_length:
                chunk_id = data[offset:offset+4]
                chunk_size = struct.unpack('<I', data[offset+4:offset+8])[0]

                chunk_start = offset + 8
                chunk_end = chunk_start + chunk_size

                if chunk_end > data_length:
                    # Corrupted chunk size
                    break

                chunk_data = data[chunk_start:chunk_end]
                chunks.append((chunk_id, offset, chunk_size, chunk_data))

                # Handle padding (chunks are aligned to even sizes)
                offset = chunk_end
                if chunk_size % 2 == 1:
                    offset += 1

    except Exception as e:
        return f"Error parsing {file_path}: {e}"
    return chunks

def parse_png_chunks(file_path):
    """Parses chunks in a PNG file."""
    chunks = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()

            if data[:8] != b'\x89PNG\r\n\x1a\n':
                return None

            offset = 8
            while offset + 8 < len(data):
                length = struct.unpack(">I", data[offset:offset+4])[0]
                chunk_type = data[offset+4:offset+8]
                chunk_data = data[offset+8:offset+8+length]
                chunks.append((chunk_type, offset, length, chunk_data))
                offset += length + 12
    except Exception as e:
        return f"Error parsing {file_path}: {e}"
    return chunks

def parse_chunks(file_path):
    """Detects file format and extracts chunks accordingly."""
    if file_path.lower().endswith((".jpg", ".jpeg")):
        return parse_jpeg_chunks(file_path)
    elif file_path.lower().endswith(".webp"):
        return parse_webp_chunks(file_path)
    elif file_path.lower().endswith(".png"):
        return parse_png_chunks(file_path)
    return f"Unsupported file format: {file_path}"

def compare_files(file_paths, output_file="output10.txt"):
    """Compares image files by analyzing their chunks and exports the results."""
    results = []
    all_chunks = {}

    for file_path in file_paths:
        chunks = parse_chunks(file_path)
        if isinstance(chunks, str) or chunks is None:
            results.append(str(chunks))
        else:
            all_chunks[file_path] = chunks
            results.append(f"File: {file_path}")
            results.append("Chunks:")
            for marker, offset, length, _ in chunks:
                results.append(f"  Marker: {marker} | Offset: {offset} | Length: {length}")
            results.append("-" * 60)

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
        for (file1, file2), chunks_shared in common_chunks.items():
            results.append(f"Common Chunks between {file1} and {file2}:")
            for marker, offset, length, data in chunks_shared:
                results.append(f"  Marker: {marker} | Offset in {file1}: {offset} | Length: {length}")
                hexdata = binascii.hexlify(data).decode()
                results.append(f"  Chunk Data (Hex): {hexdata}")
            results.append("-" * 60)

    with open(output_file, "w") as f:
        f.write("\n".join(results))
    print(f"Comparison results written to {output_file}")

if __name__ == "__main__":
    directory = "./image_files/DallEOTGP"
    file_paths = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.lower().endswith((".jpg", ".jpeg", ".webp", ".png"))
    ]

    if not file_paths:
        print("No supported image files found in the directory.")
    else:
        print(f"Comparing {len(file_paths)} image files...")
        compare_files(file_paths)
