from enum import Enum, IntEnum, auto
from itertools import product
from random import randint
import re
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class ShopActions(IntEnum):
    products = auto()
    address = auto()
    root = auto()


class ShopCbData(CallbackData, prefix='shop'):
    action:  ShopActions


class ProductActions(IntEnum):
    details = auto()
    update = auto()
    delete = auto()


class ProductCallbackData(CallbackData, prefix='product'):
    action: ProductActions
    id: int
    title: str
    price: int


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


def build_products_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Back to root',
        callback_data=ShopCbData(action=ShopActions.root).pack(),
    )
    for idx, (name, price) in enumerate([
        ('laptop', 1299),
        ('desktop', 2499),
        ('tablet', 9999),
    ],  
    start=1):
        builder.button(
            text=name,
            callback_data=ProductCallbackData(
                action=ProductActions.details,
                id=idx,
                title=name,
                price=price,
            ),
        )
    builder.adjust(1)
    return builder.as_markup()


def product_details_kb(product_cb_data: ProductCallbackData):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='⬅️ back to products',
        callback_data=ShopCbData(action=ShopActions.products).pack(),
    )
    for label, action in [
        ("Update", ProductActions.update), 
        ("Delete", ProductActions.delete)
        ]:
        pass
        builder.button(
            text=label,
            callback_data=ProductCallbackData(
                action=action,
                id=product_cb_data.id,
                title=product_cb_data.title,    
                price=product_cb_data.price,    
            ),
        )
    builder.adjust(1,2)
    return builder.as_markup()