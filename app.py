import os
import sqlite3
from flask import Flask, render_template, request, redirect, session
from datetime import date

app = Flask(__name__)
app.secret_key = "secret123"

# -------- DATABASE PATH ----------
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

# -------- HOME ----------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    records = conn.execute("SELECT * FROM attendance").fetchall()
    conn.close()

    return render_template("index.html", records=records)

# -------- REGISTER ----------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = "student"

        conn = get_db()
        conn.execute(
            "INSERT INTO users(username,email,password,role) VALUES (?,?,?,?)",
            (username,email,password,role)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# -------- LOGIN ----------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin")
            else:
                return redirect("/")

    return render_template("login.html")

# -------- ADMIN PANEL ----------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/")

    conn = get_db()
    students = conn.execute("SELECT * FROM users WHERE role='student'").fetchall()
    conn.close()

    return render_template("admin.html", students=students)

# -------- MARK ATTENDANCE ----------
@app.route("/mark/<int:id>/<status>")
def mark(id,status):
    if session.get("role") != "admin":
        return redirect("/")

    today = date.today()

    conn = get_db()
    conn.execute(
        "INSERT INTO attendance(student_id,status,date) VALUES (?,?,?)",
        (id,status,today)
    )
    conn.commit()
    conn.close()

    return redirect("/admin")

# -------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------- INIT DATABASE ----------
init_db()

# -------- RUN APP ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
