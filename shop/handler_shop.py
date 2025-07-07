from calendar import c
from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import markdown

from shop import keyboards_shop


handler = Router()

@handler.message(Command('shop'))
async def send_shop_message_w_kb(message: Message):
    await message.answer(
        text='Your shop actions: ',
        reply_markup=keyboards_shop.build_shop_kb(),
    )

@handler.callback_query(
        keyboards_shop.ShopCbData.filter(F.action == keyboards_shop.ShopActions.address)
)
async def shop_kb_callback_handlers_address(callback_query: CallbackQuery):
    await callback_query.answer(
        text="Your address section is still in progress...",
        cache_time=30,                                
                    )
    

@handler.callback_query(
        keyboards_shop.ShopCbData.filter(F.action == keyboards_shop.ShopActions.products)
)
async def shop_kb_callback_handlers_products(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text='Available products:',
        reply_markup=keyboards_shop.build_products_kb(),
        )
    

@handler.callback_query(
        keyboards_shop.ShopCbData.filter(F.action == keyboards_shop.ShopActions.root)
)
async def shop_kb_callback_handlers_root(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text='Your shop actions: ',
        reply_markup=keyboards_shop.build_shop_kb(),                       
                    )
    

@handler.callback_query(
        keyboards_shop.ProductCallbackData.filter(F.action == keyboards_shop.ProductActions.details)
)
async def shop_kb_callback_handlers_details(
    callback_query: CallbackQuery,
    callback_data: keyboards_shop.ProductCallbackData,
 ):
    await callback_query.answer()
    message_text = markdown.text(
        markdown.hbold(f"Product #{callback_data.id}"),
        markdown.text(
            markdown.hbold(f"Title: "),
            callback_data.title,
        ),
        markdown.text(
            markdown.hbold(f"Price: "),
            callback_data.price,
        ),
        sep="\n",
    )
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=keyboards_shop.product_details_kb(callback_data),
                    )