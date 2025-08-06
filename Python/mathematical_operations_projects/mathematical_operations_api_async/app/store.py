import aiosqlite
import json
from datetime import datetime


db_name = "operations.db"


async def init_db():
    async with aiosqlite.connect(db_name) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS OPERATIONS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                OPERATION TEXT NOT NULL,
                PARAMETERS TEXT NOT NULL,
                RESULT TEXT NOT NULL,
                TIMESTAMP TEXT NOT NULL
            )
        """)
        await db.commit()


async def save_request(operation: str, parameters: dict, result: dict):
    async with aiosqlite.connect(db_name) as db:
        await db.execute("""
            INSERT INTO OPERATIONS (OPERATION, PARAMETERS, RESULT, TIMESTAMP)
            VALUES (?, ?, ?, ?)
        """, (
            operation,
            json.dumps(parameters),
            json.dumps(result),
            datetime.now().isoformat()
        ))
        await db.commit()


async def fetch_history():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("""
            SELECT * FROM OPERATIONS
        """) as cursor:
            return await cursor.fetchall()
