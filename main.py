import asyncio
import os 
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv
import logging
from commands_menu import set_commands
# from handlers import handler              ####ОТКЛЮЧИЛ ОСНОВНЫЕ ХЭНДЛЕРЫ
# from shop.handler_shop import handler
from FSM.handler_FSM import handler 

load_dotenv(find_dotenv())




bot = Bot(token=f'{os.getenv("TOKEN")}', parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(handler)

async def start(bot: Bot):
    await bot.send_message(chat_id=f'{os.getenv("CHAT_ID")}', text='бот запущен')


async def stop(bot: Bot):
    await bot.send_message(chat_id=f'{os.getenv("CHAT_ID")}', text='бот остановлен')


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await set_commands(bot) 
    dp.startup.register(start)
    dp.shutdown.register(stop)
    await dp.start_polling(bot) 


if __name__ == "__main__":
    asyncio.run(main())