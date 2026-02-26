import sqlite3

DB_PATH = "Student_Marks_Dataset.db"

marks_rows = [
    (101, "Arnav",     "Science", 1, 88),
    (102, "Sonakshi", "Science", 1, 92),
    (103, "Roy",       "English", 2, 85),
    (104, "Sanya",     "Maths",   2, 91),
    (105, "Rahul",     "Science", 1, 76),
    (106, "Riya",      "English", 3, 89),
    (107, "Aman",      "Maths",   3, 90),
    (108, "Neha",      "Science", 2, 83),
    (109, "Tushar",    "English", 1, 78),
    (110, "Kriti",     "Maths",   2, 95),
]

kv_seed = [
    ("subject", "SANSKRIT"),
    ("subject", "ART"),
    ("class",   "4"),
    ("class",   "5"),
]

doc_key = "APP_INTRO"
doc_text = "Hello! This is your app intro.\nYou can edit any line via the kvdoc API."

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS marks;
    DROP TABLE IF EXISTS kv_store;

    CREATE TABLE marks (
        roll   INTEGER PRIMARY KEY,
        name   TEXT,
        subject TEXT,
        class  INTEGER,
        marks  INTEGER
    );

    CREATE TABLE kv_store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key_name  TEXT NOT NULL,
        value_text TEXT NOT NULL,
        UNIQUE(key_name, value_text)
    );
    """)

    cur.executemany(
        "INSERT INTO marks (roll, name, subject, class, marks) VALUES (?, ?, ?, ?, ?)",
        marks_rows
    )

    for key_name, value_text in kv_seed:
        cur.execute(
            "INSERT OR IGNORE INTO kv_store (key_name, value_text) VALUES (?, ?)",
            (key_name, value_text)
        )

    cur.execute(
        "INSERT INTO kv_store (key_name, value_text) VALUES (?, ?)",
        (doc_key, doc_text)
    )

    conn.commit()
    conn.close()
    print("✅ Database seeded: marks + kv_store ready!")

if __name__ == "__main__":
    main()