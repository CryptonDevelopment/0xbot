from . import *
from helpers import api


async def top_up_balance(
    query: CallbackQuery, state: FSMContext, bot: Bot, user: User
) -> None:
    await state.clear()

    msg = await query.message.answer(
        text = await safe_for_markdown(payment_msgs.type),
        reply_markup=await top_up_balance_kb.top_up_balance()
    )

    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])
    await query.answer("")


async def top_up_balance_bank_card(
    query: CallbackQuery, state: FSMContext, bot: Bot, user: User
) -> None:
    await state.clear()

    msg = await query.message.answer(
        await safe_for_markdown(payment_msgs.bank_card_type_message),
        reply_markup=await about_prime_kb.back_keyboard("top_up_balance"),
    )

    await state.update_data({"payment_type": "card"})
    await state.set_state(states.TopUpBalance.amount)

    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])
    await query.answer("")


async def top_up_balance_crypto_token(
    query: CallbackQuery, state: FSMContext, bot: Bot, user: User
) -> None:
    await state.clear()

    msg = await query.message.answer(
        await safe_for_markdown(payment_msgs.top_up_balance_crypto_token),
        reply_markup=await top_up_balance_kb.top_up_balance_crypto_methods(),
    )
    await state.update_data({"payment_type": "crypto"})
    await state.set_state(states.TopUpBalance.token)

    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id])
    await query.answer("")


async def top_up_balance_crypto_network(
    query: CallbackQuery, state: FSMContext, bot: Bot, user: User
) -> None:
    data = query.data.split("__")[1]

    await query.message.edit_text(
        await safe_for_markdown(payment_msgs.top_up_balance_crypto_network.format(data),),
        reply_markup=await top_up_balance_kb.top_up_balance_crypto_methods("network", data),
    )

    await state.update_data({"token": data})
    await state.set_state(states.TopUpBalance.network)
    await query.answer("")


async def top_up_balance_crypto_amount(
    query: CallbackQuery, state: FSMContext, bot: Bot, user: User
) -> None:

    network = query.data.split("__")[1]
    token = (await state.get_data()).get("token")

    await query.message.edit_text(
        await safe_for_markdown(payment_msgs.top_up_balance_crypto_amount.format(token,network)),
        reply_markup=await about_prime_kb.back_keyboard("top_up_balance"),
    )
    await state.update_data({"network": network})
    await state.set_state(states.TopUpBalance.amount)
    await query.answer("")


async def top_up_balance_url(
    message: Message, state: FSMContext, bot: Bot, user: User
) -> None:
    user_data = await user_helpers.check_user(message)

    if "," in (amount := message.text):
        amount = amount.replace(",", ".")

    try:
        amount = float(amount)
    except Exception as error:
        msg = await message.answer("Укажите число")
        await delete_msg_to_delete(user.id)
        await add_msg_to_delete(user.id, [msg.message_id, message.message_id])
        return

    state_data = await state.get_data()
    payment_type = state_data.get("payment_type", "crypto")
    url = f"/api/v1/top-up-balance/?user_id={user_data['id']}"
    data = {"amount": amount, "payment_type": payment_type}
    if payment_type == "card":
        data["currency"] = "RUB"
    elif payment_type == "crypto":
        data["currency"] = state_data["token"]
        data["network"] = state_data["network"]

    data = await api.post_request(url=url, data=data)
    url = data["paymentUrl"]

    msg = await message.answer(
        await safe_for_markdown(payment_msgs.top_up_balance_url),
        reply_markup=await top_up_balance_kb.top_up_balance_url(url=url),
        disable_web_page_preview=True,
    )

    if state:
        await state.clear()
    await delete_msg_to_delete(user.id)
    await add_msg_to_delete(user.id, [msg.message_id, message.message_id])
