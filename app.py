from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn

# HOME PAGE
@app.route("/")
def home():
    return redirect("/login")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match"

        conn = get_db()
        conn.execute(
            "INSERT INTO users(username,email,password,role) VALUES(?,?,?,?)",
            (username, email, password, "student")
        )
        conn.commit()
        conn.close()
        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password),
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]
            session["user_id"] = user["id"]

            if user["role"] == "admin":
                return redirect("/admin")
            else:
                return redirect("/student")

        return "Invalid username or password"

    return render_template("login.html")

# ADMIN DASHBOARD
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied"

    conn = get_db()
    students = conn.execute(
        "SELECT * FROM users WHERE role='student'"
    ).fetchall()
    attendance = conn.execute(
        """
        SELECT attendance.student_id,
               users.username,
               attendance.status,
               attendance.date
        FROM attendance
        JOIN users ON attendance.student_id = users.id
        """
    ).fetchall()
    conn.close()

    return render_template("admin.html", students=students, attendance=attendance)

# STUDENT DASHBOARD
@app.route("/student")
def student():
    if session.get("role") != "student":
        return "Access Denied"

    conn = get_db()
    attendance = conn.execute(
        """
        SELECT attendance.student_id,
               users.username,
               attendance.status,
               attendance.date
        FROM attendance
        JOIN users ON attendance.student_id = users.id
        """
    ).fetchall()
    conn.close()

    return render_template("student.html", attendance=attendance)

# MARK ATTENDANCE (ADMIN ONLY)
@app.route("/mark/<int:id>/<status>")
def mark(id, status):
    if session.get("role") != "admin":
        return "Access Denied"

    today = date.today()
    conn = get_db()
    conn.execute(
        "INSERT INTO attendance(student_id,status,date) VALUES(?,?,?)",
        (id, status, today)
    )
    conn.commit()
    conn.close()

    return redirect("/admin")

# DELETE STUDENT + DELETE ATTENDANCE
@app.route("/delete/<int:id>")
def delete(id):
    if session.get("role") != "admin":
        return "Access Denied"

    conn = get_db()
    conn.execute("DELETE FROM attendance WHERE student_id=?", (id,))
    conn.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# DATABASE SETUP
if __name__ == "__main__":
    conn = sqlite3.connect("attendance.db")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT,
            role TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            status TEXT,
            date TEXT
        )
        """
    )
    conn.close()
    app.run(debug=True)