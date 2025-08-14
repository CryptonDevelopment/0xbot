from . import *
from helpers import api


async def top_up_balance() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Банковская карта",
                    callback_data="bank_card",
                ),
                InlineKeyboardButton(
                    text="Криптовалюта",
                    callback_data="top_up_balance_crypto",
                ),
            ],
        ]
    )


async def top_up_balance_url(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Пополнить баланс",
                    url=url
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вступить в Prime",
                    callback_data="enter_prime_btn"
                )
            ]
        ]
    )


async def top_up_balance_crypto_methods(
    type: str = "currency", token=None
) -> InlineKeyboardMarkup:
    url = f"/api/v1/payments/available/methods"
    payment_methods = await api.get_request(url)
    inline_keyboard = []
    MAX_LINE_ITEMS = 2
    line = 0
    keys = set()
    for method in payment_methods:
        method_id = method.get("method", {}).get("id")
        if method_id == "crypto":
            key = method.get(type, {}).get("id")
            if (
                key in keys
                or token
                and method.get("currency", {}).get("id") != token
            ):
                continue
            keys.add(key)

            if (
                len(inline_keyboard) > line
                and len(inline_keyboard[line]) < MAX_LINE_ITEMS
            ):
                inline_keyboard[line].append(
                    InlineKeyboardButton(
                        text=key,
                        callback_data=f"crypto_{type}__{key}",
                    )
                )
            else:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=key, callback_data=f"crypto_{type}__{key}"
                        )
                    ]
                )
                if len(inline_keyboard[line]) == MAX_LINE_ITEMS:
                    line += 1

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)