import sqlite3

conn = sqlite3.connect("mess.db")
cur = conn.cursor()

# ---------------- TABLES ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    id TEXT PRIMARY KEY,
    name TEXT,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS complaints(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    complaint TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS menu(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    breakfast TEXT,
    lunch TEXT,
    dinner TEXT
)
""")

conn.commit()

# ---------------- ADMIN ----------------
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


# ---------------- SAMPLE STUDENTS (1 to 10) ----------------
def add_sample_students():
    for i in range(1, 11):
        sid = str(i)                 # 1 to 10
        name = f"Student{i}"
        password = f"pass{i}"       # pass1 to pass10

        try:
            cur.execute(
                "INSERT INTO students VALUES(?,?,?)",
                (sid, name, password)
            )
        except:
            pass

    conn.commit()


# ---------------- STUDENT FUNCTIONS ----------------
def register():
    sid = input("Student ID: ")
    name = input("Name: ")
    password = input("Password: ")

    try:
        cur.execute("INSERT INTO students VALUES(?,?,?)", (sid, name, password))
        conn.commit()
        print("✅ Registered Successfully")
    except:
        print("❌ ID already exists")


def student_login():
    sid = input("Student ID: ")
    password = input("Password: ")

    cur.execute("SELECT * FROM students WHERE id=? AND password=?", (sid, password))
    user = cur.fetchone()

    if user:
        print("\n✅ Welcome", user[1])
        student_dashboard(sid)
    else:
        print("❌ Invalid Login")


def student_dashboard(sid):
    while True:
        print("\n===== STUDENT DASHBOARD =====")
        print("1. View Menu")
        print("2. Add Complaint")
        print("3. View My Complaints")
        print("4. Logout")

        ch = input("Enter choice: ")

        if ch == "1":
            cur.execute("SELECT * FROM menu")
            rows = cur.fetchall()

            if rows:
                print("\n--- MENU ---")
                for r in rows:
                    print("\nDay:", r[1])
                    print("Breakfast:", r[2])
                    print("Lunch:", r[3])
                    print("Dinner:", r[4])
            else:
                print("No Menu Available")

        elif ch == "2":
            complaint = input("Enter Complaint: ")

            cur.execute(
                "INSERT INTO complaints(student_id, complaint) VALUES(?,?)",
                (sid, complaint)
            )
            conn.commit()
            print("✅ Complaint Submitted")

        elif ch == "3":
            cur.execute("SELECT * FROM complaints WHERE student_id=?", (sid,))
            rows = cur.fetchall()

            if rows:
                for r in rows:
                    print("\nID:", r[0])
                    print("Complaint:", r[2])
                    print("Status:", r[3])
            else:
                print("No Complaints")

        elif ch == "4":
            break


# ---------------- ADMIN FUNCTIONS ----------------
def admin_login():
    u = input("Admin Username: ")
    p = input("Password: ")

    if u == ADMIN_USER and p == ADMIN_PASS:
        print("\n✅ Admin Login Successful")
        admin_dashboard()
    else:
        print("❌ Invalid Admin Login")


def admin_dashboard():
    while True:
        print("\n===== ADMIN DASHBOARD =====")
        print("1. Add Menu")
        print("2. View Complaints")
        print("3. Update Complaint Status")
        print("4. View Students (1-10)")
        print("5. Logout")

        ch = input("Enter choice: ")

        if ch == "1":
            day = input("Day: ")
            b = input("Breakfast: ")
            l = input("Lunch: ")
            d = input("Dinner: ")

            cur.execute(
                "INSERT INTO menu(day, breakfast, lunch, dinner) VALUES(?,?,?,?)",
                (day, b, l, d)
            )
            conn.commit()
            print("✅ Menu Added")

        elif ch == "2":
            cur.execute("SELECT * FROM complaints")
            rows = cur.fetchall()

            for r in rows:
                print("\nID:", r[0])
                print("Student:", r[1])
                print("Complaint:", r[2])
                print("Status:", r[3])

        elif ch == "3":
            cid = input("Complaint ID: ")
            status = input("New Status (Pending/Resolved): ")

            cur.execute("UPDATE complaints SET status=? WHERE id=?", (status, cid))
            conn.commit()
            print("✅ Updated")

        elif ch == "4":
            cur.execute("SELECT * FROM students LIMIT 10")
            rows = cur.fetchall()

            print("\n--- STUDENTS ---")
            for r in rows:
                print("ID:", r[0], "Name:", r[1])

        elif ch == "5":
            break


# ---------------- MAIN MENU ----------------
add_sample_students()

while True:
    print("\n===== MESS MANAGEMENT SYSTEM =====")
    print("1. Student Register")
    print("2. Student Login")
    print("3. Admin Login")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        register()

    elif choice == "2":
        student_login()

    elif choice == "3":
        admin_login()

    elif choice == "4":
        conn.close()
        print("👋 System Closed")
        break

    else:
        print("❌ Invalid Choice")