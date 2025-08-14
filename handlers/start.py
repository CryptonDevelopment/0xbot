from . import *


async def start_1(message: Message, state: FSMContext, bot: Bot, user: User) -> None:
    await user_helpers.check_user(message)
    #await TimerMessage.filter(user = user).delete()
    msg1 = await message.answer_video_note(
        video_note=FSInputFile(path="videos/1.mp4")
    )
    msg2 = await message.answer(
        text = await safe_for_markdown(start_msgs.start_msg_1),
        reply_markup = await start_kb.start_kb_message_1()
    )

    await create_timer_message(user, DELAY_DAYS_2, "start_2")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [message.message_id, msg1.message_id, msg2.message_id])


async def start_2(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "start_2")

    msg1 = await bot.send_video_note(
        chat_id=user.id,
        video_note=FSInputFile(path="videos/2.mp4")
    )
    msg2 = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(start_msgs.start_msg_2),
        reply_markup = await start_kb.start_kb_message_2()
    )

    await create_timer_message(user, DELAY_MINUTES_5, "start_3")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg1.message_id, msg2.message_id])


async def start_3(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "start_3")

    msg1 = await bot.send_video_note(
        chat_id=user.id,
        video_note=FSInputFile(path="videos/3.mp4")
    )
    msg2 = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(start_msgs.start_msg_3),
        reply_markup = await start_kb.to_select_type_keyboard()
    )
    await create_timer_message(user, DELAY_MINUTES_5, "select_type")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg1.message_id, msg2.message_id])
