# src/api.py

import requests
from src.config import API_URL, DEFAULT_HEADERS

def fetch_users(session: str, page: int, size: int, positions: list, account_types: list) -> dict | None:
    url = f"{API_URL}?page={page}&size={size}"

    payload = {
        "searchStr": "",
        "positionCodes": positions,
        "accountTypes": account_types
    }

    headers = DEFAULT_HEADERS.copy()
    cookies = {
        "SESSION": session
    }

    try:
        response = requests.post(url, headers=headers, json=payload, cookies=cookies, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Ошибка при запросе: {e}")
        return None
