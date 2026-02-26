from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "Student_Marks_Dataset.db"
TABLE_NAME = "marks"
KV_TABLE = "kv_store"

# ----------------- DB Helpers -----------------

def ensure_kv_table():
    """Create kv_store if not exists"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {KV_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT NOT NULL,
            value_text TEXT NOT NULL,
            UNIQUE(key_name, value_text)
        )
    """)
    conn.commit()
    conn.close()

def save_doc_text(key_name, full_text):
    """Always keep only the latest version for each key (overwrite old)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # delete any old entries for this key
    cur.execute(f"DELETE FROM {KV_TABLE} WHERE key_name = ?", (key_name,))
    # insert the new value
    cur.execute(f"INSERT INTO {KV_TABLE}(key_name, value_text) VALUES(?, ?)", (key_name, full_text))
    conn.commit()
    conn.close()

def get_latest_doc_text(key_name):
    """Get latest text for a key"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"""
        SELECT value_text FROM {KV_TABLE}
        WHERE key_name = ?
        ORDER BY id DESC
        LIMIT 1
    """, (key_name,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

def get_all_keys():
    """Return all keys stored"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT key_name FROM {KV_TABLE}")
    keys = [r[0] for r in cur.fetchall()]
    conn.close()
    return keys

def get_columns():
    """Get column names from the main table (marks)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({TABLE_NAME})")
    cols = [row[1] for row in cur.fetchall()]
    conn.close()
    return cols

def parse_line_suffix(raw_key):
    """Split MYDOC_LINE1 → (MYDOC, 1)"""
    k = raw_key.upper()
    if "_LINE" in k:
        try:
            base, tail = k.rsplit("_LINE", 1)
            return base, int(tail)
        except ValueError:
            return raw_key, None
    return raw_key, None

# ----------------- Subject APIs -----------------

@app.route("/subjects", methods=["GET"])
def list_subjects():
    """List all subjects for all classes"""
    ensure_kv_table()
    keys = get_all_keys()
    subjects = {}
    for k in keys:
        if "::" in k:
            cls, subj = k.split("::", 1)
            subjects.setdefault(cls, []).append(subj)
    return jsonify(subjects)

@app.route("/subject/<cls>", methods=["POST"])
def add_subjects(cls):
    """Add subjects with syllabus for a class"""
    ensure_kv_table()
    data = request.get_json(silent=True) or {}

    if "subjects" not in data or not isinstance(data["subjects"], dict):
        return jsonify({"error": "Send JSON with 'subjects': { 'Subject': 'syllabus text', ... }"}), 400

    added = {}
    for subj, syllabus in data["subjects"].items():
        key = f"{cls}::{subj}"
        save_doc_text(key, syllabus)
        added[subj] = syllabus

    return jsonify({"message": f"Subjects added/updated for Class {cls}", "subjects": added})

@app.route("/subject/<cls>/<name>", methods=["GET"])
def get_subject(cls, name):
    """Get syllabus of one subject"""
    ensure_kv_table()
    key = f"{cls}::{name}"
    text = get_latest_doc_text(key)
    if text == "":
        return jsonify({"error": f"No syllabus found for {name} in Class {cls}"}), 404
    return jsonify({"class": cls, "subject": name, "syllabus": text})

@app.route("/subject/<cls>/<name>", methods=["DELETE"])
def delete_subject(cls, name):
    """Delete a subject"""
    ensure_kv_table()
    key = f"{cls}::{name}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {KV_TABLE} WHERE key_name = ?", (key,))
    deleted_rows = cur.rowcount
    conn.commit()
    conn.close()

    if deleted_rows == 0:
        return jsonify({"error": f"No subject '{name}' found in Class {cls}"}), 404
    return jsonify({"message": f"Subject '{name}' deleted from Class {cls}"})

# ----------------- KV APIs -----------------

@app.route("/kv/<key>", methods=["GET"])
def kv_read(key):
    ensure_kv_table()
    columns = get_columns()
    match = next((c for c in columns if c.lower() == key.lower()), None)
    if not match:
        return jsonify({"error": f"'{key}' is not a valid column. Valid: {columns}"}), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT {match} FROM {TABLE_NAME} WHERE {match} IS NOT NULL")
    db_vals = [str(r[0]) for r in cur.fetchall()]
    cur.execute(f"SELECT value_text FROM {KV_TABLE} WHERE key_name = ?", (match,))
    kv_vals = [str(r[0]) for r in cur.fetchall()]
    conn.close()

    seen, merged = set(), []
    for v in db_vals + kv_vals:
        if v not in seen:
            seen.add(v)
            merged.append(v)

    return jsonify({match: merged})

@app.route("/kv/<key>", methods=["POST"])
def kv_write(key):
    ensure_kv_table()
    columns = get_columns()
    match = next((c for c in columns if c.lower() == key.lower()), None)
    if not match:
        return jsonify({"error": f"'{key}' is not a valid column. Valid: {columns}"}), 400

    data = request.get_json(silent=True) or {}
    values = []
    if "value" in data:
        values = [data["value"]]
    elif "values" in data and isinstance(data["values"], list):
        values = data["values"]
    else:
        return jsonify({"error": "Send JSON with 'value' or 'values' (list)."}), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for v in values:
        v_str = str(v).strip()
        if v_str:
            cur.execute(f"INSERT OR IGNORE INTO {KV_TABLE}(key_name, value_text) VALUES(?,?)",
                        (match, v_str))
    conn.commit()
    conn.close()

    return kv_read(match)

# ----------------- KVDoc APIs -----------------

@app.route("/kvdoc/<key>", methods=["GET"])
def kvdoc_read(key):
    ensure_kv_table()
    base_key, line_no = parse_line_suffix(key)
    full_text = get_latest_doc_text(base_key)

    if full_text == "":
        return jsonify({"error": f"No value found for key '{base_key}'"}), 404

    lines = full_text.splitlines()
    if line_no is None:
        return jsonify({"key": base_key, "text": full_text, "lines": lines, "line_count": len(lines)})

    idx = line_no - 1
    if idx < 0 or idx >= len(lines):
        return jsonify({"error": f"Line {line_no} not found for key '{base_key}'"}), 404

    return jsonify({"key": f"{base_key}_LINE{line_no}", "line": line_no, "text": lines[idx]})

@app.route("/kvdoc/<key>", methods=["POST"])
def kvdoc_write(key):
    ensure_kv_table()
    base_key, line_no_from_key = parse_line_suffix(key)
    data = request.get_json(silent=True) or {}

    if "set_text" in data:
        new_text = str(data["set_text"])
        save_doc_text(base_key, new_text)
        return jsonify({"message": "Document updated", "key": base_key,
                        "line_count": len(new_text.splitlines())})

    line_no = line_no_from_key or int(data.get("line", 0))
    if line_no <= 0:
        return jsonify({"error": "Provide a valid 1-based 'line' or use _LINEX in URL"}), 400

    full_text = get_latest_doc_text(base_key)
    lines = full_text.splitlines() if full_text != "" else []

    while len(lines) < line_no:
        lines.append("")

    insert_at = data.get("insert_at", None)
    new_segment = str(data.get("text", ""))
    current = lines[line_no - 1]

    if insert_at is None:
        lines[line_no - 1] = new_segment
        op = "line_replaced"
    else:
        i = max(0, min(int(insert_at), len(current)))
        lines[line_no - 1] = current[:i] + new_segment + current[i:]
        op = "inserted_into_line"

    updated_text = "\n".join(lines)
    save_doc_text(base_key, updated_text)

    return jsonify({"message": "Document updated", "operation": op,
                    "key": base_key, "line": line_no,
                    "new_line_text": lines[line_no - 1]})

# ----------------- Dynamic / Filter -----------------

@app.route("/<page>")
def dynamic_data(page):
    param = request.args.get("params")
    if not param:
        return jsonify({"error": "Missing 'params' query"}), 400

    columns = get_columns()
    match = next((c for c in columns if c.lower() == page.lower()), None)
    if not match:
        return jsonify({"error": f"'{page}' is not a valid column. Valid: {columns}"}), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE {match} = ?", (param,))
    rows = cur.fetchall()
    col_names = [d[0] for d in cur.description]
    conn.close()

    if not rows:
        return jsonify({"message": f"No data found for {match} = {param}"}), 404

    results = [dict(zip(col_names, r)) for r in rows]
    return jsonify({f"{match}={param}": results})

@app.route("/filter")
def filter_class_subject():
    param = request.args.get("params")
    if not param or "_" not in param:
        return jsonify({"error": "Expected: class_subject (e.g. 1_Science)"}), 400

    class_part, subject_part = param.split("_", 1)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE class = ? AND subject = ?", (class_part, subject_part))
    rows = cur.fetchall()
    col_names = [d[0] for d in cur.description]
    conn.close()

    if not rows:
        return jsonify({"message": f"No records for Class {class_part}, Subject {subject_part}"}), 404

    results = [dict(zip(col_names, r)) for r in rows]
    return jsonify({f"class={class_part}_subject={subject_part}": results})

# ----------------- Run -----------------

if __name__ == "__main__":
    ensure_kv_table()
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)