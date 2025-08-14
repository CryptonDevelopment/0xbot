from models import TimerMessage
from bot_setup import bot, logger
import time
from handlers.start import start_2, start_3
from handlers.problems_types import select_type, selected_type_info
import handlers.about_prime as about_prime
import asyncio


HANDLER_MAP = {
    "start_2": start_2,
    "start_3": start_3,
    "select_type": select_type,
    "selected_type_info": selected_type_info,
    "about_prime1": about_prime.about_prime1,
    "about_prime2": about_prime.about_prime2,
    "about_prime3": about_prime.about_prime3,
    "prime_reminder1": about_prime.prime_reminder1,
    "prime_reminder2": about_prime.prime_reminder2,
    "prime_reminder3": about_prime.prime_reminder3,
    "need_gift2": about_prime.need_gift2,
    "prime_notif": about_prime.prime_notif
}


async def process_timer_messages():
    while True:
        timer_messages = await TimerMessage.filter(active = True).prefetch_related('user')
        #timer_messages = await TimerMessage.all().prefetch_related('user')
        for timer_message in timer_messages:
            time_now = int(time.time())
            if time_now > timer_message.created + timer_message.timer:
                try:
                    handler = HANDLER_MAP.get(timer_message.after)
                    await handler(query=None, state=None, bot = bot, user = timer_message.user)
                
                except Exception as e:
                    logger.error(e)

        await asyncio.sleep(5)