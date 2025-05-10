# main.py
import time
import json
import argparse
from src import api, db, parser, utils
from src.config import DEFAULT_POSITION_CODES, DEFAULT_ACCOUNT_TYPES, PAGE_SIZE
from src.logger import logger

def main():
    # Аргументы командной строки
    arg_parser = argparse.ArgumentParser(description="TenChat user fetcher")
    arg_parser.add_argument("--start-page", type=int, help="Стартовая страница (если не указана, берётся из БД progress)")
    arg_parser.add_argument("--end-page", type=int, help="Конечная страница (если не указана, идёт по лимиту из настроек)")
    args = arg_parser.parse_args()

    session = input("Введите SESSION cookie: ").strip()

    settings = db.get_settings()
    request_limit = settings["request_limit"]
    delay_min = settings["delay_min_sec"]
    delay_max = settings["delay_max_sec"]

    # Вычисляем стартовую и конечную страницы
    page = args.start_page if args.start_page else db.get_progress()
    end_page = args.end_page if args.end_page else (page + request_limit - 1)

    i = 0
    while page <= end_page:
        logger.info(f"🔄 Запрос {i + 1}, страница {page}")
        start_time = time.time()

        response = api.fetch_users(session, page, PAGE_SIZE, DEFAULT_POSITION_CODES, DEFAULT_ACCOUNT_TYPES)
        if not response:
            logger.warning("⚠️ Ошибка запроса или пустой ответ. Остановлено.")
            break

        duration = round(time.time() - start_time, 2)
        logger.info(f"⏱ Ответ получен за {duration} сек.")
        logger.debug("📦 Ответ от API:")
        # logger.debug(json.dumps(response, indent=2, ensure_ascii=False))

        users = parser.parse_users(response)
        logger.info(f"👤 Найдено пользователей: {len(users)}")

        if users:
            logger.info("💾 Сохраняю пользователей в БД...")
            db.save_users(users)
        else:
            logger.warning("⚠️ Пользователи не найдены. Пропуск сохранения.")

        db.log_request(session_token=session, page=page, response_time=duration, user_count=len(users))
        db.set_progress(page + 1)

        page += 1
        i += 1

        if page > end_page:
            logger.info("📌 Достигнута конечная страница.")
            break

        utils.sleep_random(delay_min, delay_max)

    logger.info("✅ Завершено. Проверьте базу данных.")

if __name__ == "__main__":
    main()
