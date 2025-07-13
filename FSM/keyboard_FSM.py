from ctypes import resize
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from email_validator import validate_email, EmailNotValidError


def build_yes_or_no_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="yes")
    builder.button(text="no")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def valid_email_filter(message: Message):
    try:
        email = validate_email(message.text)
    except EmailNotValidError:
        return None
    return {"email": email.normalized}


def valid_email(text):
    try:
        email = validate_email(text)
    except EmailNotValidError:
        return None
    return email.normalized


def valid_email_message_text(message: Message):
    return valid_email(message.text)

