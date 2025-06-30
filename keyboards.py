from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


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