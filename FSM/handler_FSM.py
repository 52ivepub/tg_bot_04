from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.fsm.state import StatesGroup, State


handler = Router()




class Survey(StatesGroup):
    full_name = State()




@handler.message(Command('survey'))
async def handle_start(message: Message, state: FSMContext):
    await state.set_state(Survey.full_name)
    await message.answer(
        text="Welcome to our weekly survey, Whats your name ?"
    )


@handler.message(Survey.full_name, F.text)
async def handler_survey_user_full_name(message: Message):
    await message.answer(
        f"Hello {markdown.hbold(message.text)}",
        parse_mode=ParseMode.HTML,
         
    )

@handler.message(Survey.full_name)
async def handle_survey_user_full_name_invalid_content_type(message: Message):
    await message.answer(
        "Sorry, I didn't understand, send your full name as text"
    )
