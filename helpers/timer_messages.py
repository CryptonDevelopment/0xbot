from models import TimerMessage
from bot_setup import bot, logger
import time
from datetime import datetime, timezone
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


TIMED = {
    "prime_reminder1": datetime(2025, 8, 21, 12, 0, 0, tzinfo=timezone.utc),  # 21 августа в 12:00 UTC
    "prime_reminder2": datetime(2025, 8, 28, 12, 0, 0, tzinfo=timezone.utc),  # 28 августа в 12:00 UTC
    "prime_reminder3": datetime(2025, 8, 31, 12, 0, 0, tzinfo=timezone.utc),  # 31 августа в 12:00 UTC
}


async def process_timer_messages():
    while True:
        timer_messages = await TimerMessage.filter(active=True).prefetch_related('user')
        
        current_time = datetime.now(timezone.utc)
        
        for timer_message in timer_messages:
            time_now = int(time.time())
            
            if timer_message.after in TIMED:
                scheduled_time = TIMED[timer_message.after]
                if current_time >= scheduled_time:
                    try:
                        handler = HANDLER_MAP.get(timer_message.after)
                        if handler:
                            await handler(query=None, state=None, bot=bot, user=timer_message.user)
                    except Exception as e:
                        logger.error(f"Error executing timed handler {timer_message.after}: {e}")
            
            elif time_now > timer_message.created + timer_message.timer:
                try:
                    handler = HANDLER_MAP.get(timer_message.after)
                    if handler:
                        await handler(query=None, state=None, bot=bot, user=timer_message.user)
                except Exception as e:
                    logger.error(f"Error executing timer handler {timer_message.after}: {e}")

        await asyncio.sleep(5)