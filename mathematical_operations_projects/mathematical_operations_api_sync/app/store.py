import sqlite3
import json
from datetime import datetime


db_name = "operations.db"


def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OPERATIONS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            OPERATION TEXT NOT NULL,
            PARAMETERS TEXT NOT NULL,
            RESULT TEXT NOT NULL,
            TIMESTAMP TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_request(operation: str, parameters: dict, result: dict):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO OPERATIONS (OPERATION, PARAMETERS, RESULT, TIMESTAMP)
        VALUES (?, ?, ?, ?)
    """, (
        operation,
        json.dumps(parameters),
        json.dumps(result),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


def fetch_history():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM OPERATIONS
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
