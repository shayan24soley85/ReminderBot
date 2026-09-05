import sqlite3


def init_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            age TEXT,
            phone TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_user(chat_id, name, age, phone):
    conn = sqlite3.connect("bot_data.db")
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
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, age, phone FROM users WHERE chat_id = ?", (chat_id,))
    user = cursor.fetchone()

    conn.close()
    return user


def delete_user(chat_id):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE chat_id = ?", (chat_id,))

    conn.commit()
    conn.close()
