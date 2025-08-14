from aiogram.client.default import DefaultBotProperties
import config
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisEventIsolation, RedisStorage
from aiogram.types import Update, CallbackQuery, Message, TelegramObject
from typing import Any, Awaitable, Callable, Dict, Union
from logger_setup import get_logger
from models import User
from time import time


class ChatTypeMiddleware:
    async def __call__(self, handler, event: Update, data: dict):
        if event.message:
            chat_type = event.message.chat.type
            if chat_type in ["group", "supergroup", "channel"]:
                return
        return await handler(event, data)


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        if event.message:
            telegram_user = event.message.from_user
            message = event.message
        elif event.callback_query:
            telegram_user = event.callback_query.from_user
            message = event.callback_query.message

        username = (
            telegram_user.username
            if telegram_user.username
            else str(telegram_user.id)
        )
        user = await User.get_or_none(id=telegram_user.id)

        if not user:
            id = telegram_user.id
            lang = "ru" if "ru" in telegram_user.language_code else "en"
            user = await User.create(
                id=id,
                username=username,
                lang= lang
            )

        elif user.username != username:
            user.username = username
        
        user.last_seen = int(time())
        await user.save()

        data["user"] = user

        return await handler(event, data)


bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode='MARKDOWNV2'))

storage = RedisStorage.from_url(config.REDIS_URL)
isolation = RedisEventIsolation.from_url(config.REDIS_URL)

dp = Dispatcher(storage=storage, events_isolation=isolation)

dp.update.middleware(ChatTypeMiddleware())
dp.update.middleware(UserCheckMiddleware())


logger = get_logger("Bot")
