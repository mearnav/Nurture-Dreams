import sqlite3
from datetime import datetime
from database import DB_NAME

def fetch_logs_for_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT action, details, start_time, end_time
        FROM activity_log
        WHERE user_id = ?
        ORDER BY start_time
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()

    log_list = []
    for row in rows:
        log_list.append({
            "action": row[0],
            "details": row[1],
            "start_time": row[2],
            "end_time": row[3]
        })
    return log_list

def log_activity(user_id, action, details=""):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE activity_log
        SET end_time = ?
        WHERE user_id = ? AND end_time IS NULL
    """, (start_time, user_id))

    cur.execute("""
        INSERT INTO activity_log (user_id, action, details, start_time)
        VALUES (?, ?, ?, ?)
    """, (user_id, action, details, start_time))

    conn.commit()
    conn.close()


def update_last_action_end(user_id):
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE activity_log
        SET end_time = ?
        WHERE user_id = ? AND end_time IS NULL
    """, (end_time, user_id))

def get_full_user_report(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get user info
    cur.execute("SELECT id, full_name, email, created_at FROM users WHERE username = ?", (username,))
    user = cur.fetchone()

    if not user:
        conn.close()
        return None

    user_id = user[0]
    full_name = user[1]
    email = user[2]
    signup_time = user[3]

    # Get all logs
    cur.execute("""
        SELECT action, details, start_time, end_time
        FROM activity_log
        WHERE user_id = ?
        ORDER BY start_time
    """, (user_id,))
    logs = cur.fetchall()
    conn.close()

    # Calculate total time spent
    total_seconds = 0
    activity_list = []
    for row in logs:
        start = row[2]
        end = row[3]
        duration = 0
        if end:
            duration = (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds()
            total_seconds += duration

        activity_list.append({
            "action": row[0],
            "details": row[1],
            "start_time": start,
            "end_time": end,
            "duration_sec": round(duration, 2)
        })

    return {
        "username": username,
        "full_name": full_name,
        "email": email,
        "signup_time": signup_time,
        "total_time_spent_seconds": round(total_seconds, 2),
        "activity_log": activity_list
    }

    conn.commit()
    conn.close()