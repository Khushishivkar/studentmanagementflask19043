import sqlite3
from datetime import date

# Connect to database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Delete old users and attendance
c.execute("DELETE FROM attendance")
c.execute("DELETE FROM users")

# Add admin
c.execute("INSERT INTO users (username, email, password, name, age, course, city, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
          ("admin1", "admin1@example.com", "admin123", "Admin User", 30, "AdminCourse", "Mumbai", "admin"))

# Add students
c.execute("INSERT INTO users (username, email, password, name, age, course, city, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
          ("student1", "student1@example.com", "pass123", "Student One", 20, "BCA", "Mumbai", "student"))
c.execute("INSERT INTO users (username, email, password, name, age, course, city, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
          ("student2", "student2@example.com", "pass123", "Student Two", 21, "BSc", "Pune", "student"))

# Add attendance for students
c.execute("INSERT INTO attendance (student_id, status, date) VALUES (?, ?, ?)", (2, "Present", date.today().isoformat()))
c.execute("INSERT INTO attendance (student_id, status, date) VALUES (?, ?, ?)", (2, "Absent", "2026-03-16"))
c.execute("INSERT INTO attendance (student_id, status, date) VALUES (?, ?, ?)", (3, "Present", date.today().isoformat()))

conn.commit()
conn.close()

print("Admin and students reset successfully!")