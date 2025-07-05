import asyncio
import io
from aiogram import F, Bot, Router
from aiogram import types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
import aiohttp
import emoji

import keyboards


handler = Router()


@handler.message(Command("start"))
async def start(message: Message, bot: Bot):
    await bot.send_message(chat_id=message.chat.id, text="Wait a second...")
    await message.answer(f"Привет друг 🤗 ", reply_markup=keyboards.keyboard_start)
    await message.reply(text=f"{message.text}")


# =============СКРЫВАЕТ КЛАВИАТУРУ==============
# @handler.message(Command("delete_keyboards"))
# async def start(message: Message, bot: Bot):
#     await message.answer(f"Убрали клавиатуру 🤗 ", reply_markup=ReplyKeyboardRemove())
# ===========================
    


@handler.message(Command("help"))
async def start(message: Message, bot: Bot):
    await message.answer(f"👀 ")
    await message.answer(f"<b> Жирный </b>")
    await message.answer(f"<s> Зачеркнуто </s>")
    await message.answer(f"<ins> подчеркнуто </ins>")
    await message.answer(f"<i> Курсив </i>")
    await message.answer(f"<tg-spoiler> Спойлер </tg-spoiler>")
    await message.answer(f"<pre> Спойлер </pre>")


@handler.message(Command("help_kb"))
async def start(message: Message, bot: Bot):
    await message.answer(f"Вот цифры", reply_markup=keyboards.get_on_help_kb())


# ================КЛАВИАТУРА С ДЕЙСТВИЯМИ=============================
@handler.message(Command("more"))
async def start(message: Message, bot: Bot):
    await message.answer(f"Вот ", reply_markup=keyboards.get_actions_kb())
# =============================================    


# =============фильтр сработает только на фото с подписью===============
@handler.message(F.photo, F.caption.lower().contains("hi"))
async def get_photo(message: Message):
    await message.send_copy(chat_id=message.chat.id)


# ====================ЕСЛИ ПИШЕТ АДМИН ТО ОТВЕТИТ=================
@handler.message(
    F.from_user.id.in_({35, 1301478301}), F.text.lower().contains("i admin")
)
async def get_photo(message: Message):
    await message.answer("hi admin")


# =========ЭХО=========
# @handler.message()
# async def sticker(message: Message, bot: Bot):i
#     await message.send_copy(chat_id=message.chat.id)


# ============= ОТПРАВКА ФАЙЛА===========================
async def send_big_file(message: Message):
    file = io.BytesIO()
    url = "https://wallpapers.com/images/hd/kitty-pictures-mer7k5p1ryh4ylii.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.read()

    file.write(result)
    await message.reply_document(
        document=types.BufferedInputFile(file=file.getvalue(), filename="cat.jpg")
    )


@handler.message(Command("pic_file"))
async def send_pic_file(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    action_sender = ChatActionSender(
        bot=message.bot,
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    async with action_sender:
        await send_big_file(message)


# ================================================


# ==================ОПТРАВКА ЭМОДЗИ==============================
def is_emoji(text):
    if text:
        return all(char in emoji.EMOJI_DATA for char in text)


@handler.message(lambda message: is_emoji(message.text))
async def choose_emoji(message: Message, bot: Bot):
    # if is_emoji(message.text):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await asyncio.sleep(3)
    try:
        await message.send_copy(chat_id=message.chat.id)
    except:
        await message.answer("ЧТО ТО НЕ ВЫШЛО")


# ===========================================================


# =======================ОТПРАВКА СТИКЕРОВ====================================


@handler.message(F.sticker)
async def sticker(message: Message, bot: Bot):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.CHOOSE_STICKER,
    )
    await asyncio.sleep(3)
    await message.send_copy(chat_id=message.chat.id)


# ===============INLINE================
@handler.message(Command('callback'))
async def handle_info_command(message: Message):
    await message.answer(text='ссылки', reply_markup=keyboards.build_adtions_kb())
# ===========================================================
    

# ====================CALLBACK===========================================

@handler.callback_query(keyboards.FixedRandomNumData.filter(F.number == 66))
async def handle_target_random_number_callback(
    callback_query: CallbackQuery,
    ):
    await callback_query.answer(
        text=f'Jackpot 🎉 \n',
        cache_time=30,
    )


@handler.callback_query(keyboards.FixedRandomNumData.filter())
async def handle_fixed_random_number_callback(
    callback_query: CallbackQuery,
    callback_data: keyboards.FixedRandomNumData,
    ):
    await callback_query.answer(
        text=f'your random number is {callback_data.number}\n'
        f'callback data: {callback_query.data!r}',
        show_alert=True,
        cache_time=30,
    )
# ===========================================================