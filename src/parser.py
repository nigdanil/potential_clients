# src/parser.py

def parse_users(response_json: list) -> list[dict]:
    users = []
    for item in response_json:
        city_info = item.get("city") or {}
        picture_info = item.get("picture") or {}

        users.append({
            "id": item.get("id"),
            "name": item.get("name"),
            "surname": item.get("surname"),
            "patronymic": item.get("patronymic"),
            "username": item.get("username"),
            "position_name": item.get("position", {}).get("name"),
            "position_code": item.get("position", {}).get("code"),
            "account_type": item.get("accountType"),
            "subtype": item.get("subtype"),
            "city": city_info.get("city"),
            "country": city_info.get("country"),
            "friend_counter": item.get("friendCounter"),
            "subscriber_counter": item.get("subscriberCounter"),
            "premium": bool(item.get("premium")),
            "image_link": picture_info.get("link"),
            "image_created_at": picture_info.get("dateCreated"),
            "exported_to_1c": False
        })

    return users
