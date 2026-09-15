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


def add_course_to_user(chat_id, course_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM user_courses WHERE chat_id = ? AND course_id = ?",
        (chat_id, course_id),
    )
    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute(
        "INSERT INTO user_courses (chat_id, course_id) VALUES (?, ?)",
        (chat_id, course_id),
    )
    conn.commit()
    conn.close()
    return True


def get_user_courses(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT uc.id, uc.name, uc.course_code, uc.group_number 
        FROM user_courses 
        JOIN university_courses uc ON user_courses.course_id = uc.id 
        WHERE user_courses.chat_id = ?
    """,
        (chat_id,),
    )

    courses = cursor.fetchall()

    result = []
    for c in courses:
        result.append({"id": c[0], "name": f"{c[1]} (گروه {c[3]})"})

    conn.close()
    return result
