from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import markdown

from shop.keyboards_shop import ProductActions, ProductCallbackData, ShopActions, ShopCbData, build_products_kb, build_shop_kb, build_update_product_kb, product_details_kb


handler_shop = Router()

@handler_shop.message(Command('shop'))
async def send_shop_message_w_kb(message: Message):
    await message.answer(
        text='Your shop actions: ',
        reply_markup=build_shop_kb(),
    )

@handler_shop.callback_query(
        ShopCbData.filter(F.action == ShopActions.address)
)
async def shop_kb_callback_handlers_address(callback_query: CallbackQuery):
    await callback_query.answer(
        text="Your address section is still in progress...",
        cache_time=30,                                
                    )
    

@handler_shop.callback_query(
        ShopCbData.filter(F.action == ShopActions.products)
)
async def shop_kb_callback_handlers_products(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text='Available products:',
        reply_markup=build_products_kb(),
        )
    

@handler_shop.callback_query(
        ShopCbData.filter(F.action == ShopActions.root)
)
async def shop_kb_callback_handlers_root(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        text='Your shop actions: ',
        reply_markup=build_shop_kb(),                       
                    )
    

@handler_shop.callback_query(
        ProductCallbackData.filter(F.action == ProductActions.details)
)
async def shop_kb_callback_handlers_details(
    callback_query: CallbackQuery,
    callback_data: ProductCallbackData,
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
        reply_markup=product_details_kb(callback_data),
                    )
    


@handler_shop.callback_query(
        ProductCallbackData.filter(F.action == ProductActions.delete)
)
async def handlers_product_delete_button(
    callback_query: CallbackQuery,
):

    await callback_query.answer(
        text="Delete is still in progress..."
    )



@handler_shop.callback_query(
        ProductCallbackData.filter(F.action == ProductActions.update)
)
async def handlers_product_update_button(
    callback_query: CallbackQuery,
    callback_data: ProductCallbackData,
):

    await callback_query.answer()
    await callback_query.message.edit_reply_markup(
        reply_markup=build_update_product_kb(callback_data)
    )
    