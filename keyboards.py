from enum import Enum, IntEnum, auto
from itertools import product
from random import randint
import re
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


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
    builder = ReplyKeyboardBuilder()
    builder.button(text='location', request_location=True)
    builder.button(text='phone', request_contact=True)
    builder.button(text='poll', request_poll=KeyboardButtonPollType())
    builder.button(text='quiz', request_poll=KeyboardButtonPollType(type='quiz'))
    builder.button(text='dinner', request_poll=KeyboardButtonPollType(type='regular'))
    builder.button(text='отмена')
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


async def build_info_inline():
    drom = InlineKeyboardButton(
        text='канал',
        url='https://novosibirsk.drom.ru/'
    )
    tg_01 = InlineKeyboardButton(
        text='tg',
        url='https://t.me/ren_13_bot'
    )
    rows = [
        [drom],
        [tg_01],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


class FixedRandomNumData(CallbackData, prefix='fixed-random-num'):
    number: int    


def build_adtions_kb(random_number_button_text='Random number'):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=random_number_button_text,
        callback_data='random_num_updated_cb_data'
    )
    random_namber = randint(1, 100)
    cb_data_1 = FixedRandomNumData(number=random_namber)
    builder.button(
        text=f'Random number : {random_namber}',
        callback_data=cb_data_1.pack(),
    )
    builder.button(
        text=f'Random number : [HIDDEN]',
        callback_data=cb_data_1.pack(),
    )
    builder.adjust(1)
    return builder.as_markup()


class ShopActions(IntEnum):
    products = auto()
    address = auto()


class ShopCbData(CallbackData, prefix='shop'):
    action:  ShopActions

def build_shop_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='show products',
        callback_data=ShopCbData(action=ShopActions.products).pack(),
    )
    builder.button(
        text='address',
        callback_data=ShopCbData(action=ShopActions.address).pack(),
    )
    builder.adjust(1)
    return builder.as_markup()