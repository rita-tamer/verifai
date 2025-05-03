import sqlite3
import re

DB_PATH = "model_signatures.db"
TEXT_FILE = "common_sequences_outputPNG.txt"

# Define the model and format this file represents
MODEL_NAME = "OpenAI DallE"
FORMAT_NAME = "png"

def get_or_create_model_format_ids(cursor):
    cursor.execute("SELECT model_id FROM models WHERE model_name = ?", (MODEL_NAME,))
    row = cursor.fetchone()
    if row:
        model_id = row[0]
    else:
        cursor.execute("INSERT INTO models (model_name) VALUES (?)", (MODEL_NAME,))
        model_id = cursor.lastrowid

    cursor.execute("SELECT format_id FROM formats WHERE format_name = ?", (FORMAT_NAME,))
    row = cursor.fetchone()
    if row:
        format_id = row[0]
    else:
        cursor.execute("INSERT INTO formats (format_name) VALUES (?)", (FORMAT_NAME,))
        format_id = cursor.lastrowid

    return model_id, format_id

def hex_already_exists(cursor, model_id, format_id, chunk_hex):
    cursor.execute("""
        SELECT 1 FROM signatures
        WHERE model_id = ? AND format_id = ? AND chunk_hex = ?
    """, (model_id, format_id, chunk_hex))
    return cursor.fetchone() is not None

def load_hex_sequences(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        contents = f.read()
    return re.findall(r"Hex \(full match\): ([0-9a-fA-F]+)", contents)

def insert_sequences():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("[+] Loading hex sequences from file...")
    hex_sequences = load_hex_sequences(TEXT_FILE)
    print(f"[OK] {len(hex_sequences)} sequences found.")

    model_id, format_id = get_or_create_model_format_ids(cursor)

    count_inserted = 0
    for idx, hex_seq in enumerate(hex_sequences, start=1):
        chunk_name = f"match_in_all_{idx}"
        if not hex_already_exists(cursor, model_id, format_id, hex_seq):
            cursor.execute("""
                INSERT INTO signatures (model_id, format_id, chunk_name, chunk_hex)
                VALUES (?, ?, ?, ?)
            """, (model_id, format_id, chunk_name, hex_seq))
            count_inserted += 1

    conn.commit()
    conn.close()
    print(f"[OK] {count_inserted} new entries inserted for model '{MODEL_NAME}' and format '{FORMAT_NAME}'.")

if __name__ == "__main__":
    insert_sequences()
