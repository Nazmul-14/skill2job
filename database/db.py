# database/db.py

import os
import sqlite3

DB_PATH = "data/jobs.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
IMAGE_DIR = os.path.join(PROJECT_ROOT, "images")


def connect_db():
    return sqlite3.connect(DB_PATH)


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
        image TEXT,
        salary TEXT,
        deadline TEXT,
        job_type TEXT,
        skills_required TEXT,
        vacancy INTEGER
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        FOREIGN KEY(job_id) REFERENCES jobs(id)
    )
    """)

    conn.commit()
    conn.close()


def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    jobs = [
        ("Software Engineer", "ABC Ltd", "Dhaka",
         "Develop and maintain software applications using Python and Django.",
         os.path.join(IMAGE_DIR, "Software.png"),
         "৳40,000 - ৳60,000", "2025-06-30", "Full-time", "Python, Django, SQL", 3),

        ("Data Analyst", "XYZ Corp", "Chittagong",
         "Analyze datasets and prepare business reports using Excel and Power BI.",
         os.path.join(IMAGE_DIR, "data_analyst.png"),
         "৳35,000 - ৳50,000", "2025-07-15", "Full-time", "Excel, Power BI, SQL", 2),

        ("Web Developer", "Tech BD", "Dhaka",
         "Build frontend and backend web applications using React and Node.js.",
         os.path.join(IMAGE_DIR, "tech.png"),
         "৳45,000 - ৳70,000", "2025-06-20", "Full-time", "React, Node.js, HTML, CSS", 5),

        ("UI Designer", "Creative Studio", "Dhaka",
         "Design modern UI/UX for mobile and web applications.",
         os.path.join(IMAGE_DIR, "ui.png"),
         "৳30,000 - ৳45,000", "2025-07-01", "Part-time", "Figma, Adobe XD, Photoshop", 1),

        ("Mobile App Developer", "AppDev Ltd", "Sylhet",
         "Develop Android and iOS apps using Flutter and Dart.",
         os.path.join(IMAGE_DIR, "app.png"),
         "৳50,000 - ৳80,000", "2025-08-01", "Full-time", "Flutter, Dart, Firebase", 2),

        ("Network Engineer", "Net Solutions", "Khulna",
         "Maintain and optimize network infrastructure and security.",
         os.path.join(IMAGE_DIR, "net.png"),
         "৳35,000 - ৳55,000", "2025-07-10", "Full-time", "Networking, Cisco, Linux", 2),

        ("AI Engineer", "Smart AI", "Dhaka",
         "Research and develop machine learning and deep learning models.",
         os.path.join(IMAGE_DIR, "ai.png"),
         "৳60,000 - ৳1,00,000", "2025-07-20", "Full-time", "Python, TensorFlow, ML", 1),

        ("Database Admin", "DataSys", "Rajshahi",
         "Manage, backup and optimize relational databases.",
         os.path.join(IMAGE_DIR, "db.png"),
         "৳30,000 - ৳48,000", "2025-06-25", "Full-time", "MySQL, PostgreSQL, Oracle", 2),

        ("Cyber Security Analyst", "SecureTech", "Dhaka",
         "Protect systems and networks from cyber threats and attacks.",
         os.path.join(IMAGE_DIR, "sec.png"),
         "৳55,000 - ৳90,000", "2025-08-15", "Full-time", "Ethical Hacking, Linux, Firewall", 1),

        ("IT Support", "HelpDesk BD", "Barisal",
         "Provide technical support and troubleshooting for end users.",
         os.path.join(IMAGE_DIR, "support.png"),
         "৳20,000 - ৳30,000", "2025-07-05", "Part-time", "Hardware, Windows, Networking", 4),
    ]

    cursor.executemany("""
    INSERT INTO jobs (title, company, location, description, image,
                      salary, deadline, job_type, skills_required, vacancy)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, jobs)

    conn.commit()
    conn.close()


def get_all_jobs():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, company, location, description,
               image, salary, deadline, job_type, skills_required, vacancy
        FROM jobs
    """)
    rows = cursor.fetchall()

    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "description": row[4],
            "image": row[5],
            "salary": row[6],
            "deadline": row[7],
            "job_type": row[8],
            "skills_required": row[9],
            "vacancy": row[10]
        })

    conn.close()
    return jobs


def save_job(job_id):
    conn = connect_db()
    cursor = conn.cursor()


    cursor.execute("SELECT id FROM saved_jobs WHERE job_id = ?", (job_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO saved_jobs (job_id) VALUES (?)", (job_id,))
        conn.commit()
        result = True
    else:
        result = False

    conn.close()
    return result


def get_saved_jobs():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT j.id, j.title, j.company, j.location, j.description,
               j.image, j.salary, j.deadline, j.job_type, j.skills_required, j.vacancy
        FROM jobs j
        JOIN saved_jobs s ON j.id = s.job_id
    """)
    rows = cursor.fetchall()

    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0], "title": row[1], "company": row[2],
            "location": row[3], "description": row[4], "image": row[5],
            "salary": row[6], "deadline": row[7], "job_type": row[8],
            "skills_required": row[9], "vacancy": row[10]
        })

    conn.close()
    return jobs

def remove_saved_job(job_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_jobs WHERE job_id = ?", (job_id,))
    conn.commit()
    conn.close()


def get_user_skills(uid):
    from core.data_manager import get_user_by_id
    try:
        user = get_user_by_id(uid)
        raw_skills = user.get("skills", [])


        if isinstance(raw_skills, dict):
            all_skills = []
            for skill_list in raw_skills.values():
                all_skills.extend(skill_list)
            return all_skills


        elif isinstance(raw_skills, list):
            return raw_skills

        return []
    except:
        return []


def clear_jobs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs")
    conn.commit()
    conn.close()
