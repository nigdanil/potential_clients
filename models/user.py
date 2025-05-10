# src/models/user.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    username: Optional[str]
    position_name: Optional[str]
    position_code: Optional[int]
    account_type: Optional[str]
    subtype: Optional[str]
    city: Optional[str]
    country: Optional[str]
    friend_counter: Optional[int]
    subscriber_counter: Optional[int]
    premium: bool
    image_link: Optional[str]
    image_created_at: Optional[str]
    exported_to_1c: bool = False
