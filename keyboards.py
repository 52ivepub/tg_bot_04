import re
from aiogram.types import KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


keyboard_start = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/help"),
                KeyboardButton(text="/delete_keyboards"),
                KeyboardButton(text="/pleese"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберете кнопку",
        one_time_keyboard=True,
    )


# def get_on_help_kb():
#     numbers = [
#         '1️⃣',
#         '2️⃣',
#         '3️⃣',
#         '4️⃣',
#         '5️⃣',
#         '6️⃣',
#         '7️⃣',
#         '8️⃣',
#         '9️⃣',
#         '0️⃣',
#     ]
#     buttons_row = [KeyboardButton(text=num) for num in numbers]
#     markup = ReplyKeyboardMarkup(keyboard=[buttons_row], resize_keyboard=True, one_time_keyboard=True,)
#     return markup


def get_on_help_kb():
    numbers = [
        '1️⃣',
        '2️⃣',
        '3️⃣',
        '4️⃣',
        '5️⃣',
        '6️⃣',
        '7️⃣',
        '8️⃣',
        '9️⃣',
        '0️⃣',
    ]
    builder = ReplyKeyboardBuilder()
    for num in numbers:
        builder.button(text=num)
    builder.adjust(3, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_actions_kb():
    # markup = ReplyKeyboardMarkup(

    # )
    builder = ReplyKeyboardBuilder()
    builder.button(text='location', request_location=True)
    builder.button(text='phone', request_contact=True)
    builder.button(text='chat', request_chat=True)
    builder.button(text='poll', request_poll=KeyboardButtonPollType())
    builder.button(text='quiz', request_poll=KeyboardButtonPollType(type='quiz'))
    builder.button(text='dinner', request_poll=KeyboardButtonPollType(type='regular'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)