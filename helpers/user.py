from aiogram.types import Message
from config import API_ENDPOINT
import helpers.api as api
from typing import Optional


async def user_by_telegram_id(telegram_id: int) -> dict:
    url = f"/api/v1/users/profile?telegram_id={telegram_id}"
    return (await api.get_request(url=url))


async def register_telegram(
    telegram_id: int,
    username: Optional[str] = None,
    language_code: Optional[str] = None,
) -> dict:

    url = f"/api/v1/users/register-tg/"
    data = {
        "telegram_id": telegram_id,
        "profile_username": username if username else telegram_id,
        "telegram_username": username if username else telegram_id,
        "language_code": language_code if language_code else "ru"
    }

    return (await api.post_request(url=url, data=data))


async def check_user(data: Message, code: str = None) -> dict:
    telegram_id = data.from_user.id
    username = (
        data.from_user.username
        if data.from_user.username
        else data.from_user.id
    )
    locale = data.from_user.language_code

    result = await user_by_telegram_id(telegram_id=telegram_id)

    if not result.get("id"):
        result = await register_telegram(telegram_id, username, language_code=locale)

    return result