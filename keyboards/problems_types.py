from . import *


async def select_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Пробую всё подряд — и ничего не успеваю",
                    callback_data="type:1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Боюсь всё слить и поэтому просто наблюдаю",
                    callback_data="type:2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вижу движ, но не понимаю, с чего начать",
                    callback_data="type:3"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Освоил направление и упёрся в потолок заработка",
                    callback_data="type:4"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Другая причина",
                    callback_data="type:5"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Проблем нет, всё супер",
                    callback_data="type:6"
                ),
            ]
        ]
    )


async def about_prime_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Подробнее о Prime",
                    callback_data="about_prime_btn"
                )
            ],
        ]
    )