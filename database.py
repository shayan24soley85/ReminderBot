import sqlite3
from models import Exam, Course
from Enums import ExamType, exam_status

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            exam_type TEXT,
            date_time TEXT,
            location TEXT,
            FOREIGN KEY (course_id) REFERENCES university_courses(id)
        )
    """)

    conn.commit()
    conn.close()

    sync_course_exams()


def sync_course_exams():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, exam_date FROM university_courses 
        WHERE exam_date != 'نامشخص'
    """)
    courses = cursor.fetchall()

    for course_id, exam_date in courses:
        cursor.execute(
            "SELECT 1 FROM course_exams WHERE course_id = ? AND exam_type = ?",
            (course_id, ExamType.FINAL.value),
        )
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO course_exams (course_id, exam_type, date_time)
                VALUES (?, ?, ?)
            """,
                (course_id, ExamType.FINAL.value, exam_date),
            )

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


def remove_course_from_user(chat_id, course_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM user_courses WHERE chat_id = ? AND course_id = ?",
        (chat_id, course_id),
    )

    conn.commit()
    conn.close()


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


def get_user_exams_objects(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ce.exam_type, ce.date_time, ce.location,
               uc.name, uc.professor
        FROM user_courses ur
        JOIN university_courses uc ON ur.course_id = uc.id
        JOIN course_exams ce ON ce.course_id = uc.id
        WHERE ur.chat_id = ?
    """,
        (chat_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    exam_objects = []
    for row in rows:
        exam_type_str, date_time, location, course_name, prof = row

        course_obj = Course(name=course_name, professor=prof)

        exam_obj = Exam(
            course=course_obj,
            exam_type=ExamType(exam_type_str),
            date_time=date_time,
            exam_status=exam_status.NOT_STARTED,
            location=location,
        )
        exam_objects.append(exam_obj)

    return exam_objects


def add_exam_to_course(course_id, exam_type, date_time, location=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO course_exams (course_id, exam_type, date_time, location)
        VALUES (?, ?, ?, ?)
        """,
        (course_id, exam_type, date_time, location),
    )
    conn.commit()
    conn.close()
