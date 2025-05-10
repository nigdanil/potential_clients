# src/export.py

import sqlite3
import csv

DB_PATH = "tenchat.db"

def export_to_csv(filename="exported_users.csv", mark_as_exported=True):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Получаем невыгруженных
    cur.execute("""
        SELECT id, name, surname, patronymic, username,
               position_name, account_type, city, country,
               friend_counter, subscriber_counter, premium, image_link
        FROM users
        WHERE exported_to_1c = 0
    """)
    rows = cur.fetchall()

    if not rows:
        print("📭 Нет новых пользователей для выгрузки.")
        conn.close()
        return

    # Экспорт в CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Имя", "Фамилия", "Отчество", "Username",
            "Должность", "Тип аккаунта", "Город", "Страна",
            "Друзья", "Подписчики", "Премиум", "Фото"
        ])
        writer.writerows(rows)

    print(f"📁 Успешно выгружено: {len(rows)} записей → {filename}")

    # Обновляем статус в БД
    if mark_as_exported:
        ids = [str(row[0]) for row in rows]
        cur.execute(f"""
            UPDATE users
            SET exported_to_1c = 1
            WHERE id IN ({','.join(['?']*len(ids))})
        """, ids)
        conn.commit()

    conn.close()
