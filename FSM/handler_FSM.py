import email
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
    email = State()


def validate_email(text: str):
    if "@" not in text or "." not in text:
        raise ValueError("Invalid email")
    return text.lower()


def valid_email_filter(message: Message):
    try:
        email = validate_email(message.text)
    except ValueError:
        return None
    return {"email": email}


@handler.message(Command('survey'))
async def handle_start(message: Message, state: FSMContext):
    await state.set_state(Survey.full_name)
    await message.answer(
        text="Welcome to our weekly survey, Whats your name ?"
    )


@handler.message(Survey.full_name, F.text)
async def handler_survey_user_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(Survey.email)
    await message.answer(
        f"Hello {markdown.hbold(message.text)}, now please share your email",
        parse_mode=ParseMode.HTML,
         
    )

@handler.message(Survey.full_name)
async def handle_survey_user_full_name_invalid_content_type(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Sorry, I didn't understand, send your full name as text"
    )


@handler.message(Survey.email, valid_email_filter)
async def handler_survey_user_email(
    message: Message,
    state: FSMContext,
    email: str):
    await state.update_data(email=message.text)
    await message.answer(
        text=f"Cool yuor email is now {markdown.hcode(email)}",
    )


@handler.message(Survey.email)
async def handler_survey_invalid_email(
    message: Message):
    await message.answer(
        text=f"Invalid email", 
    )