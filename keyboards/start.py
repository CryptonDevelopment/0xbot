from . import *


async def start_kb_message_1() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Погнали !",
                    callback_data="to_start_2_btn"
                )
            ]
        ]
    )


async def start_kb_message_2() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="А потом что?",
                    callback_data="to_start_3_btn"
                )
            ]
        ]
    )


async def to_select_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Слушать дальше",
                    callback_data="select_type_btn"
                )
            ]
        ]
    )
