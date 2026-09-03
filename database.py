import sqlite3

DATABASE_NAME = "tickets.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            tags TEXT,
            created_at TEXT NOT NULL,
            response_deadline TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()