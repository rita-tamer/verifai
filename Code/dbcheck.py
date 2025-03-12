import os
import sqlite3
import binascii
import struct

DB_PATH = "model_signatures.db"

# --- 1️⃣ Retrieve Signatures from Database ---
def get_all_chunk_signatures():
    """Fetch all chunk signatures from the database and return as a list."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT m.model_name, f.format_name, s.chunk_name, s.chunk_hex
        FROM signatures s
        JOIN models m ON s.model_id = m.model_id
        JOIN formats f ON s.format_id = f.format_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    signatures = []
    for row in rows:
        try:
            model_name, format_name, chunk_name, chunk_hex = row
            chunk_bytes = binascii.unhexlify(chunk_hex.strip())  # Convert hex to bytes
            signatures.append({
                'model_name': model_name,
                'format_name': format_name,
                'chunk_name': chunk_name,
                'chunk_bytes': chunk_bytes
            })
        except binascii.Error:
            print(f"⚠️ Warning: Skipping invalid chunk_hex for {chunk_name} ({chunk_hex})")
    
    return signatures

# --- 2️⃣ Parse JPEG Chunks ---
def parse_jpeg_chunks(file_path):
    """Extracts chunks from a JPEG image."""
    chunks = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            offset = 0

            # JPEGs start with the SOI marker (FFD8)
            if data[:2] != b'\xFF\xD8':
                return None

            offset += 2
            while offset < len(data):
                if data[offset] == 0xFF:
                    marker = data[offset:offset+2]
                    if marker == b'\xFF\xD9':  # EOI (End of Image)
                        chunks.append((marker, offset, 0, b""))
                        break
                    length = struct.unpack(">H", data[offset+2:offset+4])[0]
                    chunk_data = data[offset+4:offset+4+length-2]
                    chunks.append((marker, offset, length, chunk_data))
                    offset += length + 2
                else:
                    break
    except Exception as e:
        print(f"❌ Error parsing JPEG file {file_path}: {e}")
        return None
    return chunks

# --- 3️⃣ Parse WebP Chunks ---
def parse_webp_chunks(file_path):
    """Extracts chunks from a WebP image."""
    chunks = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
                return None

            offset = 12
            while offset < len(data):
                if offset + 8 > len(data):
                    break

                chunk_id = data[offset:offset+4]
                chunk_size = struct.unpack("<I", data[offset+4:offset+8])[0]
                chunk_data = data[offset+8:offset+8+chunk_size]
                chunks.append((chunk_id, offset, chunk_size, chunk_data))
                offset += 8 + chunk_size
    except Exception as e:
        print(f"❌ Error parsing WebP file {file_path}: {e}")
        return None
    return chunks

# --- 4️⃣ Detect File Format & Parse ---
def parse_chunks(file_path):
    """Detects file format and extracts chunks accordingly."""
    lower = file_path.lower()
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return parse_jpeg_chunks(file_path)
    elif lower.endswith(".webp"):
        return parse_webp_chunks(file_path)
    else:
        print(f"❌ Unsupported file format: {file_path}")
        return None

# --- 5️⃣ Match Extracted Chunks Against Stored Signatures ---
def check_image_against_signatures(image_path, chunk_signatures):
    """
    Reads image, extracts chunks, and checks for matches in the database.
    Returns a list of (model_name, chunk_name, format_name) for all matches found.
    """
    all_chunks = parse_chunks(image_path)
    if all_chunks is None:
        return []

    matches = []
    for marker, offset, length, chunk_data in all_chunks:
        for sig in chunk_signatures:
            if sig['chunk_bytes'] in chunk_data:
                matches.append((sig['model_name'], sig['chunk_name'], sig['format_name']))

    return matches

# --- 6️⃣ Main Execution ---
def main():
    # 1️⃣ Get stored chunk signatures
    all_signatures = get_all_chunk_signatures()

    # 2️⃣ Provide the path to the uploaded image file
    uploaded_image_path = r'E:\Uni\grad project\traiced\image_files\DallEOTGJ\FruitsDallE1.jpg'  

    # 3️⃣ Check if it matches any known chunk signatures
    matches = check_image_against_signatures(uploaded_image_path, all_signatures)

    # 4️⃣ Print results
    if matches:
        print(f"\n✅ Image '{uploaded_image_path}' contains chunk signatures from:")
        for model_name, chunk_name, format_name in matches:
            print(f"   - Model: {model_name} | Format: {format_name} | Chunk: {chunk_name}")
        print("\n🔍 This image is likely AI-generated.")
    else:
        print(f"\n❌ No known AI model signatures found in '{uploaded_image_path}'.")

if __name__ == '__main__':
    main()
