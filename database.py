import sqlite3

DB_NAME = "bot_data.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            age TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS university_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT,
            group_number TEXT,
            department_id INTEGER,
            name TEXT,
            professor TEXT,
            exam_date TEXT,
            units INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (chat_id) REFERENCES users(chat_id),
            FOREIGN KEY (course_id) REFERENCES university_courses(id)
        )
    """)

    conn.commit()
    conn.close()


def save_user(chat_id, name, age, phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO users (chat_id, name, age, phone)
        VALUES (?, ?, ?, ?)
    """,
        (chat_id, name, age, phone),
    )

    conn.commit()
    conn.close()


def get_user(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, age, phone FROM users WHERE chat_id = ?", (chat_id,))
    user = cursor.fetchone()

    conn.close()
    return user


def delete_user(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE chat_id = ?", (chat_id,))

    conn.commit()
    conn.close()


def get_departments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM departments")
    deps = cursor.fetchall()
    conn.close()
    return deps


def get_courses_by_department(department_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, course_code, group_number, name, professor, exam_date, units 
        FROM university_courses 
        WHERE department_id = ?
    """,
        (department_id,),
    )
    courses = cursor.fetchall()
    conn.close()
    return courses
