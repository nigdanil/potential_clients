# src/db.py
import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "db", "tenchat.db"))


def get_connection():
    return sqlite3.connect(DB_PATH)

def get_settings() -> dict:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT request_limit, delay_min_sec, delay_max_sec FROM settings WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "request_limit": row[0],
            "delay_min_sec": row[1],
            "delay_max_sec": row[2]
        }
    return {"request_limit": 1, "delay_min_sec": 3, "delay_max_sec": 5}

def save_users(users: list[dict]):
    conn = get_connection()
    cur = conn.cursor()

    for u in users:
        cur.execute("""
            INSERT OR IGNORE INTO users (
                id, name, surname, patronymic, username,
                position_name, position_code, account_type, subtype,
                city, country, friend_counter, subscriber_counter,
                premium, image_link, image_created_at, exported_to_1c
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            u["id"], u["name"], u["surname"], u["patronymic"], u["username"],
            u["position_name"], u["position_code"], u["account_type"], u["subtype"],
            u["city"], u["country"], u["friend_counter"], u["subscriber_counter"],
            int(u["premium"]), u["image_link"], u["image_created_at"], int(u["exported_to_1c"])
        ))

    conn.commit()
    conn.close()

def log_request(session_token: str, page: int, response_time: float, user_count: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO fetch_log (session_token, requested_at, page, response_time, user_count)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session_token,
        datetime.utcnow().isoformat(),
        page,
        response_time,
        user_count
    ))

    conn.commit()
    conn.close()
