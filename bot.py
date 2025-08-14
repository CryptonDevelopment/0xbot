import asyncio
import states
from aiogram.filters import Command, StateFilter
from aiogram import F
from aiogram import Bot, Dispatcher, types
from bot_setup import bot, dp
import handlers.start as start_hadlers
import handlers.problems_types as problems_types_handlers
import handlers.about_prime as about_prime_handlers
import handlers.top_up_balance as top_up_balance_handlers
from models import init
import states
from helpers.timer_messages import process_timer_messages
import states


async def set_start_handlers() -> None:
    dp.message.register(
        start_hadlers.start_1,
        Command('start')
    )
    dp.callback_query.register(
        start_hadlers.start_2,
        F.data == "to_start_2_btn"
    )
    dp.callback_query.register(
        start_hadlers.start_3,
        F.data == "to_start_3_btn"
    )


async def set_problems_types_handlers() -> None:
    dp.callback_query.register(
        problems_types_handlers.select_type,
        F.data == "select_type_btn"
    )
    dp.callback_query.register(
        problems_types_handlers.selected_type_info,
        F.data.startswith("type")
    )

async def set_about_prime_handlers() -> None:
    dp.callback_query.register(
        about_prime_handlers.about_prime1,
        F.data == "about_prime_btn"
    )
    dp.callback_query.register(
        about_prime_handlers.about_prime2,
        F.data == "about_prime2_btn"
    )
    dp.callback_query.register(
        about_prime_handlers.about_prime3,
        F.data == "about_prime3_btn"
    )
    dp.callback_query.register(
        about_prime_handlers.enter_prime,
        F.data == "enter_prime_btn"
    )
    dp.callback_query.register(
        about_prime_handlers.enter_prime_choiсe_duration,
        F.data.startswith("sub_duration")
    )
    dp.callback_query.register(
        about_prime_handlers.enter_prime_promo,
        F.data == "enter_promo"
    )
    dp.message.register(
        about_prime_handlers.enter_prime_promo_validate,
        StateFilter(states.Promo.enter_promo)
    )
    dp.callback_query.register(
        about_prime_handlers.enter_prime_confirm,
        F.data.startswith("sub_type")
    )
    dp.callback_query.register(
        about_prime_handlers.need_help,
        F.data == "need_help_btn"
    )
    dp.callback_query.register(
        about_prime_handlers.need_gift,
        F.data == "need_gift_btn"
    )
    dp.callback_query.register(
        about_prime_handlers.download_gift,
        F.data == "download_gift"
    )


async def set_top_up_handlers() -> None:
    dp.callback_query.register(
        top_up_balance_handlers.top_up_balance,
        F.data == "top_up_balance"
    )
    dp.callback_query.register(
        top_up_balance_handlers.top_up_balance_bank_card,
        F.data == "bank_card"
    )
    dp.callback_query.register(
        top_up_balance_handlers.top_up_balance_crypto_token,
        F.data == "top_up_balance_crypto"
    )
    dp.callback_query.register(
        top_up_balance_handlers.top_up_balance_crypto_network,
        F.data.startswith("crypto_currency__"),
        StateFilter(states.TopUpBalance.token)
    )
    dp.callback_query.register(
        top_up_balance_handlers.top_up_balance_crypto_amount,
        F.data.startswith("crypto_network__")
    )
    dp.message.register(
        top_up_balance_handlers.top_up_balance_url,
        StateFilter(states.TopUpBalance.amount)
    )
    
    


async def setup_handlers() -> None:
    await set_start_handlers()
    await set_problems_types_handlers()
    await set_about_prime_handlers()
    await set_top_up_handlers()


async def main():
    await init()
    asyncio.create_task(process_timer_messages())
    await setup_handlers()
    await bot.get_updates(offset=-1)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        print("Exit")
