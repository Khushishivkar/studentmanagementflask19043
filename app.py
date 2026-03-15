import os
import sqlite3
from flask import Flask, render_template, request, redirect, session
from datetime import date

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE PATH ----------------
DB_PATH = os.path.join(os.getcwd(), "attendance.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT,
            role TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            status TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
