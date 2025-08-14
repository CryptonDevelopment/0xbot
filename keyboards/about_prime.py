from . import *


async def about_prime2_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Дальше",
                    callback_data="about_prime2_btn"
                )
            ],
        ]
    )


async def about_prime3_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="И сколько стоит ?",
                    callback_data="about_prime3_btn"
                )
            ],
        ]
    )


async def enter_prime_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Вступить в Прайм",
                    callback_data="enter_prime_btn"
                )
            ]
        ]
    )

async def enter_prime_confirm() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data="confrim_prime"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="enter_prime_btn"
                )
            ]
        ]
    )


async def not_enough_money() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Пополнить баланс",
                    callback_data="top_up_balance",
                ),
            ]
        ]
    )


async def enter_prime_choice_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Год",
                    callback_data="sub_duration:1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Месяц",
                    callback_data="sub_duration:0"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нужна помощь с выбором",
                    callback_data="need_help_btn"
                )
            ]
        ]
    )


async def choose_sub_type_keyboard(duration: int, start_id: int, pro_id: int, prime_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Start",
                    callback_data=f"sub_type:Start:{duration}:{start_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Pro",
                    callback_data=f"sub_type:Pro:{duration}:{pro_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Prime",
                    callback_data=f"sub_type:Prime:{duration}:{prime_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Указать промокод",
                    callback_data="enter_promo"
                )
            ]
        ]
    )


async def back_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=callback_data
                )
            ]
        ]
    )


async def gift_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Скачать гайд (PDF)",
                    callback_data="download_gift"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вступить в Прайм",
                    callback_data="enter_prime_btn"
                )
            ]
        ]
    )


async def about_prime4_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Вступить в Прайм",
                    callback_data="enter_prime_btn"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Нужна помощь с выбором",
                    callback_data="need_help_btn"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Хочу подарок!",
                    callback_data="need_gift_btn"
                )
            ]
        ]
    )