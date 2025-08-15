from aiogram.types import CallbackQuery
from models import MessageToDelete
from bot_setup import bot
from models import MessageToDelete, TimerMessage, User
from bot_setup import bot, logger
import time
from config import DELETE_MESSAGES


async def safe_for_markdown(text: str) -> str:
    excluded = [".", ":", "-", "~", "!", "|", "+", ">", "#", "="]
    flag = False
    text_length = len(text)
    text_new = ""
    for i in range(text_length):
        if text[i] in excluded and text[i - 1] != "\\":
            text_new += rf"\{text[i]}"
        elif text[i] == "(":
            if text[i - 1] != "]" and text[i - 1] != "\\":
                text_new += rf"\{text[i]}"
                flag = True
            else:
                text_new += text[i]
        elif text[i] == ")":
            if flag and text[i - 1] != "\\":
                text_new += rf"\{text[i]}"
                flag = False
            else:
                text_new += text[i]
        else:
            text_new += text[i]
    if "#" in text_new:
        text_new = text_new.replace("\\\\\\", "\\")

    return text_new


async def safe_query_answer(query: CallbackQuery, message: str = ""):
    try:
        await query.answer(message)
    except Exception as e:
        pass


async def add_msg_to_delete(chat_id: int, messages_ids: list[int]) -> None:
    if DELETE_MESSAGES:
        for message_id in messages_ids:
            await MessageToDelete.create(chat_id=chat_id, message_id=message_id)


async def delete_msg_to_delete(chat_id: int) -> None:
    if DELETE_MESSAGES:
        for i in await MessageToDelete.filter(chat_id=chat_id):
            try:
                await bot.delete_message(chat_id, i.message_id)
                await i.delete()
            except Exception as e:
                await i.delete()                
    

async def create_timer_message(user: User, timer: int, after: str) -> None:
    timer_message = await TimerMessage.get_or_none(user = user, after = after)
    if not timer_message:
        await TimerMessage.create(user = user, timer = timer, after = after, created = int(time.time()))


async def delete_timer_message(user: User, after: str) -> None:
    try:
        timer_message = await TimerMessage.get_or_none(user = user, after = after)
        timer_message.active = False
        await timer_message.save()
        # await timer_message.delete()
    except Exception as e:
        pass