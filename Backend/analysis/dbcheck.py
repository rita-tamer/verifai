import os
import sqlite3
import struct
import binascii
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = "model_signatures.db"

def get_all_chunk_signatures():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.signature_id, s.model_id, s.format_id, s.chunk_name, s.chunk_hex,
               m.model_name, f.format_name
        FROM signatures s
        JOIN models m ON s.model_id = m.model_id
        JOIN formats f ON s.format_id = f.format_id
    """)
    rows = cursor.fetchall()
    conn.close()

    signatures = []
    for signature_id, model_id, format_id, chunk_name, chunk_hex, model_name, format_name in rows:
        try:
            chunk_bytes = binascii.unhexlify(chunk_hex.strip())
            signatures.append({
                'signature_id': signature_id,
                'model_id': model_id,
                'model_name': model_name,
                'format_id': format_id,
                'format_name': format_name,
                'chunk_name': chunk_name,
                'chunk_bytes': chunk_bytes
            })
        except binascii.Error:
            continue
    return signatures

def parse_jpeg_chunks(file_path):
    chunks = []
    with open(file_path, "rb") as f:
        data = f.read()
        offset = 2
        while offset < len(data):
            if data[offset] == 0xFF:
                marker = data[offset:offset+2]
                if marker == b'\xFF\xD9':
                    chunks.append((marker, offset, 0, b""))
                    break
                length = struct.unpack(">H", data[offset+2:offset+4])[0]
                chunk_data = data[offset+4:offset+4+length-2]
                chunks.append((marker, offset, length, chunk_data))
                offset += length + 2
            else:
                break
    return chunks

def parse_png_chunks(file_path):
    chunks = []
    with open(file_path, "rb") as f:
        data = f.read()
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            return []

        offset = 8
        while offset + 8 < len(data):
            chunk_length = struct.unpack(">I", data[offset:offset+4])[0]
            chunk_type = data[offset+4:offset+8]
            chunk_data = data[offset+8:offset+8+chunk_length]
            chunks.append((chunk_type, offset, chunk_length, chunk_data))
            offset += 8 + chunk_length + 4
    return chunks

def parse_webp_chunks(file_path, max_bytes=64):
    matches = []
    with open(file_path, "rb") as f:
        data = f.read()
        if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
            return []

        offset = 12
        while offset + 8 <= len(data):
            chunk_type = data[offset:offset+4]
            chunk_size = struct.unpack("<I", data[offset+4:offset+8])[0]
            chunk_start = offset + 8
            chunk_end = chunk_start + chunk_size
            if chunk_end > len(data): break

            chunk_data = data[chunk_start:chunk_end]
            if (b'c2pa' in chunk_type.lower() or
                b'claimGenerator' in chunk_data[:max_bytes] or
                b'c2pa' in chunk_data[:max_bytes]):
                matches.append({
                    "chunk_type": chunk_type.decode(errors='replace'),
                    "hex": binascii.hexlify(chunk_data[:max_bytes]).decode(),
                    "ascii": chunk_data[:max_bytes].decode("utf-8", errors="replace")
                })

            offset = chunk_end + (chunk_size % 2)
    return matches

def check_against_signatures(file_path):
    signatures = get_all_chunk_signatures()
    ext = file_path.lower()

    print(f"[+] Checking {os.path.basename(file_path)}")

    if ext.endswith(".webp"):
        print("[INFO] Format: WebP")
        matches = []
        # Byte-level chunk match
        with open(file_path, "rb") as f:
            data = f.read()
            for sig in signatures:
                if sig['format_name'].lower() == "webp" and sig['chunk_bytes'] in data:
                    matches.append(sig)

        if matches:
            print("[DONE] Found matches from DB:")
            for m in matches:
                print(f"    Model: {m['model_name']} | Chunk: {m['chunk_name']}")
        else:
            print("[-] No chunk matches from DB.")

        # C2PA heuristic scan
        print("\n[+] Scanning for C2PA-like structures...")
        c2pa = parse_webp_chunks(file_path)
        if c2pa:
            for c in c2pa:
                safe_chunk_type = c['chunk_type'].encode("utf-8", errors="replace").decode("utf-8")
                safe_ascii = c['ascii'].encode("utf-8", errors="replace").decode("utf-8")
                print(f"  Chunk: {safe_chunk_type}\n    Hex: {c['hex'][:64]}...\n    ASCII: {safe_ascii}")

        else:
            print("  No C2PA-like signatures found.")

    elif ext.endswith(".jpg") or ext.endswith(".jpeg"):
        print("[INFO] Format: JPEG")
        chunks = parse_jpeg_chunks(file_path)
        for marker, offset, length, chunk_data in chunks:
            for sig in signatures:
                if sig['format_name'].lower() == "jpg" and sig['chunk_bytes'] in chunk_data:
                    print(f"[*] Match: Model={sig['model_name']} Chunk={sig['chunk_name']}")

    elif ext.endswith(".png"):
        print("[INFO] Format: PNG")
        chunks = parse_png_chunks(file_path)
        for chunk_type, offset, length, chunk_data in chunks:
            for sig in signatures:
                if sig['format_name'].lower() == "png" and sig['chunk_bytes'] in chunk_data:
                    print(f"[✓] Match: Model={sig['model_name']} Chunk={sig['chunk_name']}")

    else:
        print("[-] Unsupported file type.")

def analyze_byte_signatures(image_path):
    if not os.path.exists(image_path):
        return {
            "chunk_match": False,
            "c2pa_found": False,
            "manipulated": False
        }

    ext = image_path.lower()
    signatures = get_all_chunk_signatures()

    matches = []
    c2pa_found = False
    manipulated = False

    with open(image_path, "rb") as f:
        data = f.read()

    # Match against DB-stored chunks and collect all matches
    for sig in signatures:
        # Check both format_id and format_name for robustness
        format_matches = (sig["format_id"] == 4 and sig["format_name"].lower() == "webp")
        if format_matches and sig["chunk_bytes"] in data:
            matches.append({
                "model_id": sig["model_id"],
                "model_name": sig["model_name"]
            })

    # Set chunk_match to True only if more than 3 matches are found
    chunk_match = len(matches) > 3

    # Only applies to WebP
    if ext.endswith(".webp"):
        c2pa_chunks = parse_webp_chunks(image_path, max_bytes=128)
        if c2pa_chunks:
            c2pa_found = True

            # Heuristic: if chunk_type is broken or ascii looks garbage → possibly tampered
            for c in c2pa_chunks:
                if not c["ascii"].strip() or "����" in c["ascii"]:
                    manipulated = True
                    break
                
    return {
        "chunk_match": chunk_match,
        "matches_count": len(matches),
        "matches": matches,
        "c2pa_found": c2pa_found,
        "manipulated": manipulated
    }

if __name__ == "__main__":
    
    image_path = "./image_files/POC/FruitsDallE75.webp"
    if os.path.exists(image_path):
        check_against_signatures(image_path)
    else:
        print("[-] File not found.")
