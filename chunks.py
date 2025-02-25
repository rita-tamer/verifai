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

            # Check SOI marker
            if data[:2] != b'\xFF\xD8':
                return None

            offset += 2
            while offset < len(data):
                if data[offset] == 0xFF:
                    marker = data[offset:offset+2]
                    if marker == b'\xFF\xD9':  # EOI
                        # End Of Image
                        chunks.append((marker, offset, 0, b""))
                        break
                    # The two bytes after marker are the length (big-endian)
                    length = struct.unpack(">H", data[offset+2:offset+4])[0]
                    chunk_data = data[offset+4:offset+4+length-2]
                    chunks.append((marker, offset, length, chunk_data))
                    offset += length + 2
                else:
                    # Not a valid JPEG marker, stop parsing
                    break
    except Exception as e:
        return f"Error parsing {file_path}: {e}"
    return chunks

def parse_webp_chunks(file_path):
    """
    Parses top-level chunks in a WebP file, e.g., 'VP8 ', 'VP8L', 'VP8X', 'ALPH', 'ICCP', 'EXIF', 'XMP ', etc.
    For extended WebP ('VP8X'), you can parse sub-chunks if desired. A commented-out snippet shows how.
    """
    chunks = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            # Basic checks for WebP signature
            if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
                return None

            # The total file size is stored at offset 4, but we won't rely on it for now
            offset = 12  # skip RIFF header (4 bytes) + size (4 bytes) + 'WEBP' (4 bytes)
            data_length = len(data)

            while offset < data_length:
                # Each top-level chunk is 8 bytes of header: 4 bytes chunk_id + 4 bytes chunk_size
                if offset + 8 > data_length:
                    break

                chunk_id = data[offset:offset+4]
                chunk_size = struct.unpack('<I', data[offset+4:offset+8])[0]
                sub_start = offset + 8
                sub_end = sub_start + chunk_size
                if sub_end > data_length:
                    # Safety check to avoid going out of bounds
                    break

                chunk_data = data[sub_start:sub_end]

                # Always store the top-level chunk
                chunks.append((chunk_id, offset, chunk_size, chunk_data))

                # If you'd like to parse sub-chunks within 'VP8X', uncomment below:
                #
                if chunk_id == b'VP8X':
                    sub_offset = 0
                    # The sub-chunks would be stored consecutively in chunk_data
                    while sub_offset + 8 <= len(chunk_data):
                        sub_chunk_id = chunk_data[sub_offset:sub_offset+4]
                        sub_chunk_size = struct.unpack('<I', chunk_data[sub_offset+4:sub_offset+8])[0]
                        sub_data = chunk_data[sub_offset+8:sub_offset+8+sub_chunk_size]
                        # Add the sub-chunk to the overall chunks
                        # Use an adjusted offset (to help differentiate sub-chunks from top-level)
                        chunks.append((sub_chunk_id, offset + 8 + sub_offset, sub_chunk_size, sub_data))
                        sub_offset += 8 + sub_chunk_size

                offset = sub_end

    except Exception as e:
        return f"Error parsing {file_path}: {e}"
    return chunks

def parse_chunks(file_path):
    """Detects file format and extracts chunks accordingly."""
    if file_path.lower().endswith((".jpg", ".jpeg")):
        return parse_jpeg_chunks(file_path)
    elif file_path.lower().endswith(".webp"):
        return parse_webp_chunks(file_path)
    return f"Unsupported file format: {file_path}"

def compare_files(file_paths, output_file="output6.txt"):
    """Compares image files by analyzing their chunks and exports the results."""
    results = []
    all_chunks = {}

    # Parse all files
    for file_path in file_paths:
        chunks = parse_chunks(file_path)
        if isinstance(chunks, str) or chunks is None:  # Error message or unsupported format
            results.append(str(chunks))
        else:
            all_chunks[file_path] = chunks
            results.append(f"File: {file_path}")
            results.append("Chunks:")
            for marker, offset, length, _ in chunks:
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
        for (file1, file2), chunks_shared in common_chunks.items():
            results.append(f"Common Chunks between {file1} and {file2}:")
            for marker, offset, length, data in chunks_shared:
                results.append(f"  Marker: {marker} | Offset in {file1}: {offset} | Length: {length}")
                # Convert chunk data to hex for display
                hexdata = binascii.hexlify(data).decode()
                results.append(f"  Chunk Data (Hex): {hexdata}")
            results.append("-" * 60)

    # Write results to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(results))
    print(f"Comparison results written to {output_file}")

if __name__ == "__main__":
    directory = ".\image_files\DallEImages"
    file_paths = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.lower().endswith((".jpg", ".jpeg", ".webp"))
    ]

    if not file_paths:
        print("No supported image files found in the directory.")
    else:
        print(f"Comparing {len(file_paths)} image files...")
        compare_files(file_paths)
