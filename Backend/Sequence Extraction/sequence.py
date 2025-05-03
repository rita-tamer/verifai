import os
import binascii
import struct
from tqdm import tqdm
from collections import defaultdict

FOLDER = "./image_files/POC"
OUTPUT_FILE = "common_sequences_outputPOC.txt"
MIN_SEQUENCE_LENGTH = 12  
MAX_C2PA_SEARCH_BYTES = 256

def read_binary(path):
    with open(path, "rb") as f:
        return f.read()

def extract_c2pa_like_patterns_webp(data):
    results = []
    if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        return results

    offset = 12
    while offset + 8 < len(data):
        chunk_type = data[offset:offset+4]
        chunk_size = struct.unpack("<I", data[offset+4:offset+8])[0]
        chunk_start = offset + 8
        chunk_end = chunk_start + chunk_size
        if chunk_end > len(data): break
        chunk_data = data[chunk_start:chunk_end]
        if (b'c2pa' in chunk_type.lower() or
            b'c2pa' in chunk_data[:MAX_C2PA_SEARCH_BYTES].lower() or
            b'claimGenerator' in chunk_data[:MAX_C2PA_SEARCH_BYTES]):
            snippet = binascii.hexlify(chunk_data[:MAX_C2PA_SEARCH_BYTES]).decode()
            results.append((chunk_type.decode(errors="replace"), snippet))
        offset = chunk_end + (chunk_size % 2)
    return results

def extract_all_sequences(data, length):
    return {data[i:i+length] for i in range(len(data) - length + 1)}

def find_common_sequences_fast(file_data_dict):
    sequence_to_files = defaultdict(set)
    all_files = list(file_data_dict.keys())

    for fname in tqdm(all_files, desc="🔍 Extracting sequences"):
        data = file_data_dict[fname]
        sequences = extract_all_sequences(data, MIN_SEQUENCE_LENGTH)
        for seq in sequences:
            sequence_to_files[seq].add(fname)

    # Filter for sequences appearing in 2+ files
    common = {seq: files for seq, files in sequence_to_files.items() if len(files) > 1}
    return common

def main():
    hex_data_dict = {}
    c2pa_results = []

    files = [
        f for f in os.listdir(FOLDER)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
    ]

    print(f"[+] Scanning {len(files)} image files...\n")

    for filename in tqdm(files, desc="Reading files"):
        path = os.path.join(FOLDER, filename)
        ext = filename.lower()
        raw_data = read_binary(path)
        hex_data_dict[filename] = raw_data

        if ext.endswith(".webp"):
            c2pa = extract_c2pa_like_patterns_webp(raw_data)
            for chunk_type, snippet in c2pa:
                c2pa_results.append((filename, chunk_type, snippet))

    common_sequences = find_common_sequences_fast(hex_data_dict)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("[+] C2PA-Like Structures in WebP Files\n")
        for fname, chunk, snippet in c2pa_results:
            out.write(f"File: {fname}\nChunk: {chunk}\nHex Snippet: {snippet[:96]}...\n\n")

        out.write("\n[+] Common Byte Sequences (Hex) Found Across Multiple Images\n")
        for seq, files in common_sequences.items():
            hex_str = binascii.hexlify(seq).decode()
            out.write(f"Matched in {len(files)} files: {', '.join(files)}\n")
            out.write(f"  Hex: {hex_str[:96]}...\n\n")

        # Check for sequences present in ALL files
        out.write("\n[Done] Sequences Found in ALL Files:\n")
        total_file_count = len(hex_data_dict)
        full_matches = [
            (seq, files)
            for seq, files in common_sequences.items()
            if len(files) == total_file_count
        ]

        if full_matches:
            for seq, _ in full_matches:
                hex_full = binascii.hexlify(seq).decode()
                out.write(f"  Hex (full match): {hex_full}\n")
        else:
            out.write("  None found.\n")

    print(f"\n Done. Results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
