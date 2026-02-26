import sqlite3
import csv
from database import DB_NAME

def export_activity_log():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM activity_log")
    rows = cur.fetchall()

    with open("user_activity_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "user_id", "action", "details", "timestamp"])
        writer.writerows(rows)

    conn.close()
    print("CSV exported successfully!")

export_activity_log()