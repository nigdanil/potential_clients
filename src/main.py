import sys
import os
import time
import json
from datetime import datetime
from src import api, db, parser, utils
from src.config import DEFAULT_POSITION_CODES, DEFAULT_ACCOUNT_TYPES, PAGE_SIZE
from src.logger import logger

def main():
    session = input("Введите SESSION cookie: ").strip()

    settings = db.get_settings()
    request_limit = settings["request_limit"]
    delay_min = settings["delay_min_sec"]
    delay_max = settings["delay_max_sec"]

    page = 1
    for i in range(request_limit):
        logger.info(f"🔄 Запрос {i+1} из {request_limit}, страница {page}")

        start_time = time.time()
        response = api.fetch_users(session, page, PAGE_SIZE, DEFAULT_POSITION_CODES, DEFAULT_ACCOUNT_TYPES)

        if not response:
            logger.warning("⚠️ Ошибка запроса или пустой ответ. Остановлено.")
            break

        duration = round(time.time() - start_time, 2)
        logger.info(f"⏱ Ответ получен за {duration} сек.")

        logger.debug("📦 Ответ от API:")
        logger.debug(json.dumps(response, indent=2, ensure_ascii=False))

        users = parser.parse_users(response)
        logger.info(f"👤 Найдено пользователей: {len(users)}")

        if users:
            logger.info("💾 Сохраняю пользователей в БД...")
            db.save_users(users)
        else:
            logger.warning("⚠️ Пользователи не найдены. Пропуск сохранения.")

        db.log_request(session_token=session, page=page, response_time=duration, user_count=len(users))

        page += 1
        utils.sleep_random(delay_min, delay_max)

    logger.info("✅ Завершено. Проверьте базу данных.")

if __name__ == "__main__":
    main()
