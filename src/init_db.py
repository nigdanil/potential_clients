# init_db.py

import sqlite3

conn = sqlite3.connect("tenchat.db")
cur = conn.cursor()

# users
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    patronymic TEXT,
    username TEXT,
    position_name TEXT,
    position_code INTEGER,
    account_type TEXT,
    subtype TEXT,
    city TEXT,
    country TEXT,
    friend_counter INTEGER,
    subscriber_counter INTEGER,
    premium BOOLEAN,
    image_link TEXT,
    image_created_at TEXT,
    exported_to_1c BOOLEAN DEFAULT 0
);
""")

# settings
cur.execute("""
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    request_limit INTEGER,
    delay_min_sec INTEGER,
    delay_max_sec INTEGER
);
""")

cur.execute("""
INSERT OR IGNORE INTO settings (id, request_limit, delay_min_sec, delay_max_sec)
VALUES (1, 10, 3, 10);
""")

# fetch_log
cur.execute("""
CREATE TABLE IF NOT EXISTS fetch_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_token TEXT,
    requested_at TEXT,
    page INTEGER,
    response_time REAL,
    user_count INTEGER
);
""")

conn.commit()
conn.close()
print("✅ База данных успешно инициализирована.")
