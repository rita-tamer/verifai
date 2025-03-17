import binascii
import os

# Hex strings for the 5 chunks
chunks_hex = [
    "03010002110311003f00",
    "1100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9fa",
    "0100030101010101010101010000000000000102030405060708090a0b",
    "100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9fa",
    "0000010501010101010100000000000000000102030405060708090a0b"
]

# Convert hex to bytes
chunks_bytes = [binascii.unhexlify(h) for h in chunks_hex]

def check_chunks_in_files(directory):
    """
    Reads all .jpg, .jpeg, .webp files in 'directory' and checks if any of the
    known chunk byte sequences appear in each file.
    """
    # Gather supported files
    supported_ext = (".jpg", ".jpeg", ".webp")
    files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(supported_ext)
    ]

    if not files:
        print("No supported image files found.")
        return

    for file_path in files:
        print(f"\nFile: {file_path}")
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except Exception as e:
            print(f"  Error reading file: {e}")
            continue

        # For each chunk, check if present in file
        found_any = False
        for i, cbytes in enumerate(chunks_bytes, start=1):
            if cbytes in data:
                print(f"  Found Chunk {i}")
                found_any = True

        if not found_any:
            print("  No specified chunks found.")

# Main execution
if __name__ == '__main__':
    directory = '.\image_files\DallEOTG'
    check_chunks_in_files(directory)