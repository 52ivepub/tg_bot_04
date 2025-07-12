from ctypes import resize
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def build_yes_or_no_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="yes")
    builder.button(text="no")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)