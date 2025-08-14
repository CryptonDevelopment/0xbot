from . import *
from helpers import api


async def about_prime1(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "about_prime1")

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.about_prime),
        reply_markup = await about_prime_kb.about_prime2_keyboard()
    )

    await create_timer_message(user, DELAY_MINUTES_5, "about_prime2")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def about_prime2(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "about_prime2")

    msg1 = await bot.send_video_note(
        chat_id=user.id,
        video_note=FSInputFile(path="videos/4.mp4")
    )

    msg2 = await bot.send_photo(
        chat_id=user.id,
        photo=FSInputFile("images/screenshot.png"),
        caption = await safe_for_markdown(about_prime_msgs.about_prime2),
        reply_markup = await about_prime_kb.about_prime3_keyboard()
    )

    await create_timer_message(user, DELAY_MINUTES_15, "about_prime3")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg1.message_id, msg2.message_id])


async def about_prime3(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "about_prime3")

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.about_prime3),
        reply_markup = await about_prime_kb.about_prime4_keyboard(),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    await create_timer_message(user, DELAY_DAYS_1, "prime_reminder1")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def enter_prime(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "prime_reminder1")
    await delete_timer_message(user, "prime_reminder2")
    await delete_timer_message(user, "prime_reminder3")

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.enter_prime),
        reply_markup = await about_prime_kb.enter_prime_choice_keyboard(),
    )

    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def enter_prime_choiсe_duration(query: CallbackQuery, state: FSMContext, bot: Bot, user: User, duration: int = None) -> None:
    if duration!=0 and duration!=1:
        duration = int(query.data.split(":")[1])
        await state.update_data(duration = duration)
    
    backend_user = await user_helpers.check_user(query)  
    subs = await api.get_subs(backend_user["id"])

    discount = (await state.get_data()).get("discount")

    start_price, start_id = await api.calculate_final_price(subs.get("Start")[duration], discount)
    pro_price, pro_id = await api.calculate_final_price(subs.get("Pro")[duration], discount)
    prime_price, prime_id = await api.calculate_final_price(subs.get("Prime")[duration], discount)
    text = about_prime_msgs.enter_prime_texts[duration].format(
        start_price,
        pro_price,
        prime_price
    )

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(text),
        reply_markup = await about_prime_kb.choose_sub_type_keyboard(duration, start_id, pro_id, prime_id),
    )

    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def enter_prime_promo(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await state.set_state(states.Promo.enter_promo)
    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.enter_prime_promo),
    )
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def enter_prime_promo_validate(message: Message, state: FSMContext, bot: Bot, user: User) -> None:
    promo = message.text
    backend_user = await user_helpers.check_user(message) 
    response = await api.post_request(f"/api/v1/promo-codes/validate/?user_id={backend_user['id']}",data = {"promocode": f"{promo}"})
    if response.get("discountAmount"):
        duration = (await state.get_data()).get("duration")
        await state.update_data(discount = response)
        await enter_prime_choiсe_duration(message, state, bot, user, int(duration))
    else:
        msg = await bot.send_message(
            chat_id=user.id,
            text = await safe_for_markdown(about_prime_msgs.enter_prime_promo_error),
            reply_markup = await about_prime_kb.back_keyboard("enter_prime_btn")
        )
        await delete_msg_to_delete(user.id)
        await add_msg_to_delete(user.id, [msg.message_id, message.message_id])


async def enter_prime_confirm(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    _, type, duration, sub_id = query.data.split(":")
    backend_user = await user_helpers.check_user(query)

    if discount := (await state.get_data()).get("discount"):
        data = {"promocode": discount["code"]}
    else:
        data = {}

    response = await api.post_request(url = f"/api/v1/subscriptions/{sub_id}/buy/?user_id={backend_user['id']}", data = data)

    if response.get("code") == "insufficient_balance":
        msg1 = await query.message.answer(
            text=await safe_for_markdown(about_prime_msgs.not_enough_money),
            reply_markup=await about_prime_kb.not_enough_money(),
            disable_web_page_preview=True,
        )

        await delete_msg_to_delete(user.id)
        await add_msg_to_delete(user.id, [msg1.message_id])

    else:
        msg1 = await query.message.answer_video_note(
            video_note=FSInputFile(path="videos/5.mp4")
        )
        msg2 = await query.message.answer(
            text = await safe_for_markdown(about_prime_msgs.prime_hello_msg)
        )
        await create_timer_message(user, DELAY_MINUTES_2, "prime_notif")

        await delete_msg_to_delete(user.id)


async def prime_notif(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "prime_notif")
    await bot.send_message(
        chat_id = user.id,
        text = await safe_for_markdown(about_prime_msgs.prime_hello_notif)
    )


async def need_help(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.need_help),
        reply_markup = await about_prime_kb.back_keyboard("about_prime3_btn"),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def need_gift(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.need_gift),
        reply_markup = await about_prime_kb.gift_keyboard(),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    await create_timer_message(user, DELAY_DAYS_1, "need_gift2")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def download_gift(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await bot.send_document(
        chat_id=user.id,
        document=FSInputFile("gift/gift.pdf")
    )
    await query.answer("")


async def need_gift2(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "need_gift2")

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.need_gift2),
        reply_markup = await about_prime_kb.enter_prime_keyboard(),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def prime_reminder1(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "prime_reminder1")

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.prime_reminder1),
        reply_markup = await about_prime_kb.enter_prime_keyboard(),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    await create_timer_message(user, DELAY_DAYS_1, "prime_reminder2")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def prime_reminder2(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "prime_reminder2")

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.prime_reminder2),
        reply_markup = await about_prime_kb.enter_prime_keyboard(),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    await create_timer_message(user, DELAY_DAYS_1, "prime_reminder3")
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])


async def prime_reminder3(query: CallbackQuery, state: FSMContext, bot: Bot, user: User) -> None:
    await delete_timer_message(user, "prime_reminder3")

    msg = await bot.send_message(
        chat_id=user.id,
        text = await safe_for_markdown(about_prime_msgs.prime_reminder3),
        reply_markup = await about_prime_kb.enter_prime_keyboard(),
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )

    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])