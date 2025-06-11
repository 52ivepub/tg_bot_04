import asyncio
import os 
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv
import logging


load_dotenv(find_dotenv())



bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())