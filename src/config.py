# src/config.py

API_URL = "https://tenchat.ru/gostinder/api/web/auth/account/search/elastic"
DEFAULT_POSITION_CODES = [631]  # можно менять под фильтр
DEFAULT_ACCOUNT_TYPES = ["SELF_EMPLOYED"]
PAGE_SIZE = 20

# Заголовки для имитации браузера
DEFAULT_HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://tenchat.ru",
    "referer": "https://tenchat.ru/search/people?positions=631&accounts=SELF_EMPLOYED",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
}
