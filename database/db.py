# import sqlite3
#
# DB_PATH = "data/jobs.db"
import os
import sqlite3

DB_PATH = "data/jobs.db"

# 🔥 base folder (db.py যেখানে আছে)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 project root (db folder থেকে 1 level up)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# 🔥 images folder path
IMAGE_DIR = os.path.join(PROJECT_ROOT, "images")


# 🔹 1. Connect Database
def connect_db():
    return sqlite3.connect(DB_PATH)


# 🔹 2. Create Table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        description TEXT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()


# 🔹 3. Insert Sample Data
def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    jobs = [
        ("Software Engineer", "ABC Ltd", "Dhaka",
         "Develop and maintain software applications using Python.",
         os.path.join(IMAGE_DIR, "Software.png")),

        ("Data Analyst", "XYZ Corp", "Chittagong",
         "Analyze datasets and prepare reports.",
         os.path.join(IMAGE_DIR, "data_analyst.png")),

        ("Web Developer", "Tech BD", "Dhaka",
         "Build frontend and backend web applications.",
         os.path.join(IMAGE_DIR, "tech.png")),

        ("UI Designer", "Creative Studio", "Dhaka",
         "Design modern UI/UX for applications.",
         os.path.join(IMAGE_DIR, "ui.png")),

        ("Mobile App Developer", "AppDev Ltd", "Sylhet",
         "Develop Android apps using Flutter.",
         os.path.join(IMAGE_DIR, "app.png")),

        ("Network Engineer", "Net Solutions", "Khulna",
         "Maintain network infrastructure.",
         os.path.join(IMAGE_DIR, "net.png")),

        ("AI Engineer", "Smart AI", "Dhaka",
         "Work on machine learning models.",
         os.path.join(IMAGE_DIR, "ai.png")),

        ("Database Admin", "DataSys", "Rajshahi",
         "Manage databases and optimize queries.",
         os.path.join(IMAGE_DIR, "db.png")),

        ("Cyber Security Analyst", "SecureTech", "Dhaka",
         "Protect systems from cyber threats.",
         os.path.join(IMAGE_DIR, "sec.png")),

        ("IT Support", "HelpDesk BD", "Barisal",
         "Provide IT support and troubleshooting.",
         os.path.join(IMAGE_DIR, "support.png"))
    ]

    cursor.executemany("""
    INSERT INTO jobs (title, company, location, description, image)
    VALUES (?, ?, ?, ?, ?)
    """, jobs)

    conn.commit()
    conn.close()


# 🔹 4. Fetch Data
def get_all_jobs():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT title, company, location, description, image FROM jobs")
    rows = cursor.fetchall()

    jobs = []
    for row in rows:
        jobs.append({
            "title": row[0],
            "company": row[1],
            "location": row[2],
            "description": row[3],
            "image": row[4]
        })

    conn.close()
    return jobs

# delete
def clear_jobs():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs")  # সব data remove

    conn.commit()
    conn.close()