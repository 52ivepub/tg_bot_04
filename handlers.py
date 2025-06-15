from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message



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


# =========ЭХО=========
@handler.message()
async def sticker(message: Message, bot: Bot):
    await message.send_copy(chat_id=message.chat.id)












 