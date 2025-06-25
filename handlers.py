import io
from multiprocessing.context import assert_spawning
from aiogram import F, Bot, Router
from aiogram import types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
import aiohttp



handler = Router()


@handler.message(Command('start'))
async def start(message: Message, bot: Bot):
    await bot.send_message(chat_id=message.chat.id, text='Wait a second...')
    await message.answer(f'Привет друг 🤗 ')
    await message.reply(text=f"{message.text}")
    

@handler.message(Command('help'))
async def start(message: Message, bot: Bot):
    await message.answer(f'👀 ')
    await message.answer(f'<b> Жирный </b>')
    await message.answer(f'<s> Зачеркнуто </s>') 
    await message.answer(f'<ins> подчеркнуто </ins>') 
    await message.answer(f'<i> Курсив </i>') 
    await message.answer(f'<tg-spoiler> Спойлер </tg-spoiler>') 
    await message.answer(f'<pre> Спойлер </pre>') 


#=============фильтр сработает только на фото с подписью===============
@handler.message(F.photo, F.caption.lower().contains('hi'))
async def get_photo(message: Message):
    await message.send_copy(chat_id=message.chat.id)


# ====================ЕСЛИ ПИШЕТ АДМИН ТО ОТВЕТИТ=================
@handler.message(F.from_user.id.in_({35, 1301478301}), F.text.lower().contains('i admin'))
async def get_photo(message: Message):
    await message.answer('hi admin')

# =========ЭХО=========
# @handler.message()
# async def sticker(message: Message, bot: Bot):i
#     await message.send_copy(chat_id=message.chat.id)


async def send_big_file(message: Message):
    file = io.BytesIO()
    url = 'https://wallpapers.com/images/hd/kitty-pictures-mer7k5p1ryh4ylii.jpg'
    async with aiohttp.ClientSession() as session:
        async with session.get(url)  as response:
            result = await response.read()

    
    file.write(result)
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue(),
            filename='cat.jpg'
        )
    )


@handler.message(Command('pic_file'))
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












 