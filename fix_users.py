import sqlite3
from datetime import date

conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Create tables if not exist
c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
email TEXT,
password TEXT,
name TEXT,
age INTEGER,
course TEXT,
city TEXT,
role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id INTEGER,
status TEXT,
date TEXT
)
""")

# Clear existing data
c.execute("DELETE FROM attendance")
c.execute("DELETE FROM users")

# Admin
c.execute("""
INSERT INTO users (username,email,password,name,age,course,city,role)
VALUES (?,?,?,?,?,?,?,?)
""", ("admin1","admin1@example.com","admin123","Admin User",30,"AdminCourse","Mumbai","admin"))

# Students
c.execute("""
INSERT INTO users (username,email,password,name,age,course,city,role)
VALUES (?,?,?,?,?,?,?,?)
""", ("student1","student1@example.com","pass123","Student One",20,"BCA","Mumbai","student"))

c.execute("""
INSERT INTO users (username,email,password,name,age,course,city,role)
VALUES (?,?,?,?,?,?,?,?)
""", ("student2","student2@example.com","pass123","Student Two",21,"BSc","Pune","student"))

# Attendance
c.execute("INSERT INTO attendance (student_id,status,date) VALUES (?,?,?)",
          (2,"Present",date.today().isoformat()))

c.execute("INSERT INTO attendance (student_id,status,date) VALUES (?,?,?)",
          (2,"Absent","2026-03-16"))

c.execute("INSERT INTO attendance (student_id,status,date) VALUES (?,?,?)",
          (3,"Present",date.today().isoformat()))

conn.commit()
conn.close()

print("Admin and students reset successfully!")
