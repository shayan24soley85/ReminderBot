import os
import sqlite3
import pandas as pd
from database import init_db

DB_NAME = "bot_data.db"
DATA_DIR = "courses_data"

DEPARTMENT_MAP = {
    "CE": {"id": 40, "name": "مهندسی کامپیوتر"},
    "CV": {"id": 20, "name": "مهندسی عمران"},
}


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_department(cursor, dep_id, dep_name):
    cursor.execute(
        """
        INSERT OR IGNORE INTO departments (id, name)
        VALUES (?, ?)
    """,
        (dep_id, dep_name),
    )


def process_excel_file(filepath, dep_id):
    print(f"Processing {filepath}...")
    df = pd.read_excel(filepath, header=1)

    conn = get_connection()
    cursor = conn.cursor()

    count = 0
    for index, row in df.iterrows():
        if pd.isna(row.get("نام درس")):
            continue

        course_name = str(row.get("نام درس")).strip()
        course_code = str(row.get("شماره درس")).replace(".0", "").strip()
        group_number = str(row.get("گروه")).replace(".0", "").strip()
        professor = (
            str(row.get("نام استاد1")) if pd.notna(row.get("نام استاد1")) else "نامشخص"
        )
        units = int(row.get("واحد")) if pd.notna(row.get("واحد")) else 0
        exam_date = (
            str(row.get("تاریخ امتحان")).strip()
            if pd.notna(row.get("تاریخ امتحان"))
            else "نامشخص"
        )

        cursor.execute(
            """
            INSERT INTO university_courses 
            (course_code, group_number, department_id, name, professor, exam_date, units)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                course_code,
                group_number,
                dep_id,
                course_name,
                professor,
                exam_date,
                units,
            ),
        )
        count += 1

    conn.commit()
    conn.close()
    print(f"Successfully added {count} courses from {filepath}.")


def main():
    init_db()

    if not os.path.exists(DATA_DIR):
        print(f"Error: Folder '{DATA_DIR}' does not exist.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            dep_key = filename.split(".")[0].upper()

            if dep_key in DEPARTMENT_MAP:
                dep_info = DEPARTMENT_MAP[dep_key]
                init_department(cursor, dep_info["id"], dep_info["name"])
                conn.commit()

                filepath = os.path.join(DATA_DIR, filename)
                process_excel_file(filepath, dep_info["id"])
            else:
                print(
                    f"Skipping {filename}: Department mapping for '{dep_key}' not found in script."
                )

    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
