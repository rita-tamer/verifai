import os
import sqlite3
import struct
import binascii

DB_PATH = "model_signatures.db"

def get_all_chunk_signatures():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.model_name, f.format_name, s.chunk_name, s.chunk_hex
        FROM signatures s
        JOIN models m ON s.model_id = m.model_id
        JOIN formats f ON s.format_id = f.format_id
    """)
    rows = cursor.fetchall()
    conn.close()

    signatures = []
    for model_name, format_name, chunk_name, chunk_hex in rows:
        try:
            chunk_bytes = binascii.unhexlify(chunk_hex.strip())
            signatures.append({
                'model_name': model_name,
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

def parse_webp_chunks(file_path):
    chunks = []
    with open(file_path, "rb") as f:
        data = f.read()
        if data[:4] != b'RIFF' or data[8:12] != b'WEBP':
            return []

        offset = 12
        while offset + 8 <= len(data):
            chunk_id = data[offset:offset+4]
            chunk_size = struct.unpack("<I", data[offset+4:offset+8])[0]
            chunk_data = data[offset+8:offset+8+chunk_size]
            chunks.append((chunk_id, offset, chunk_size, chunk_data))
            offset += 8 + chunk_size
    return chunks

def parse_chunks(file_path):
    lower = file_path.lower()
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return parse_jpeg_chunks(file_path)
    elif lower.endswith(".webp"):
        return parse_webp_chunks(file_path)
    return []

def check_image_against_signatures(image_path, chunk_signatures):
    all_chunks = parse_chunks(image_path)
    matches = []
    for marker, offset, length, chunk_data in all_chunks:
        for sig in chunk_signatures:
            if sig['chunk_bytes'] in chunk_data:
                matches.append((sig['model_name'], sig['chunk_name'], sig['format_name']))
    return matches

def scan_c2pa_structures(file_path, max_bytes=64):
    results = []
    with open(file_path, "rb") as f:
        data = f.read()
        if data[0:4] != b'RIFF' or data[8:12] != b'WEBP':
            return []

        offset = 12
        while offset + 8 <= len(data):
            chunk_type = data[offset:offset+4]
            chunk_size = struct.unpack("<I", data[offset+4:offset+8])[0]
            chunk_start = offset + 8
            chunk_end = chunk_start + chunk_size
            if chunk_end > len(data):
                break

            chunk_data = data[chunk_start:chunk_end]
            offset = chunk_end
            if chunk_size % 2 == 1:
                offset += 1

            if (b'c2pa' in chunk_type.lower() or 
                b'"c2pa"' in chunk_data or 
                b'claimGenerator' in chunk_data):
                results.append({
                    "chunk_type": chunk_type.decode(errors='replace'),
                    "hex": binascii.hexlify(chunk_data[:max_bytes]).decode(),
                    "ascii": chunk_data[:max_bytes].decode("utf-8", errors="replace")
                })
    return results

def analyze_byte_signatures(file_path):
    if file_path.lower().endswith(".webp"):
        matches = scan_c2pa_structures(file_path)
        return {"c2pa_found": bool(matches)}
    else:
        signatures = get_all_chunk_signatures()
        matches = check_image_against_signatures(file_path, signatures)
        return {"chunk_match": bool(matches)}
