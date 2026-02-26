import sqlite3
import hashlib
from database import DB_NAME

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(data):
    full_name = data.get("full_name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([full_name, username, email, password]):
        return {"success": False, "message": "All fields are required"}

    password_hash = hash_password(password)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (full_name, username, email, password_hash)
            VALUES (?, ?, ?, ?)
        """, (full_name, username, email, password_hash))
        conn.commit()
        return {"success": True, "message": "User registered successfully"}
    except sqlite3.IntegrityError:
        return {"success": False, "message": "Username or email already exists"}
    finally:
        conn.close()

def login_user(data):
    username = data.get("username")
    password = data.get("password")

    if not all([username, password]):
        return {"success": False, "message": "Username and password required"}

    password_hash = hash_password(password)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    row = cur.fetchone()
    conn.close()

    if row:
        return {"success": True, "message": "Login successful", "user_id": row[0]}
    else:
        return {"success": False, "message": "Invalid username or password"}

def get_user_id_by_username(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None