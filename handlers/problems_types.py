from helpers.messages import safe_query_answer
from . import *


async def select_type(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "select_type")

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(start_msgs.select_type_msg),
        reply_markup = await problems_types_kb.select_type_keyboard()
    )

    await create_timer_message(user, DELAY_HOUR_1, "selected_type_info")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])
    await safe_query_answer(query)


async def selected_type_info(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "selected_type_info")
    if query:
        type = int(query.data.split(":")[1])
    else:
        type = 6

    MESSAGE_MAP = {
        1:problem_messages.problem1,
        2:problem_messages.problem2,
        3:problem_messages.problem3,
        4:problem_messages.problem4,
        5:problem_messages.problem5,
        6:problem_messages.problem6,
    }

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(MESSAGE_MAP.get(type)),
        reply_markup = await problems_types_kb.about_prime_keyboard()
    )

    await create_timer_message(user, DELAY_HOUR_1, "about_prime1")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])
    await safe_query_answer(query)