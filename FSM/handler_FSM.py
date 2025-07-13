import email
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import markdown
from aiogram.fsm.state import StatesGroup, State
from email_validator import validate_email, EmailNotValidError

from FSM.keyboard_FSM import build_yes_or_no_keyboard, valid_email_filter, valid_email, valid_email_message_text

handler = Router()


class Survey(StatesGroup):
    full_name = State()
    email = State()
    email_news_later = State()


@handler.message(Command('survey'))
async def handle_start(message: Message, state: FSMContext):
    await state.set_state(Survey.full_name)
    await message.answer(
        text="Welcome to our weekly survey, Whats your name ?",
        reply_markup=ReplyKeyboardRemove(),
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


@handler.message(Survey.email, F.text.cast(validate_email).normalized.as_("email"))
async def handler_survey_user_email(
    message: Message,
    state: FSMContext,
    email: str):
    await state.update_data(email=message.text)
    await state.set_state(Survey.email_news_later)
    await message.answer(
        text=f"Cool yuor email is now {markdown.hcode(email)}\n"
        "Would you like to be contacted in future", 
        reply_markup=build_yes_or_no_keyboard()
    )


@handler.message(Survey.email)
async def handler_survey_invalid_email(
    message: Message):
    await message.answer(
        text=f"Invalid email", 
    )


# @handler.message(Survey.email)
# async def handler_my_option(
#     message: Message,
#     state: FSMContext,
#     ):
#     await state.update_data(email=message.text)
#     await state.set_state(Survey.email_news_later)
#     try:
#         validate_email(message.text)
#         return await message.answer(
#             text=f"Cool yuor email is now {markdown.hcode(email)}\n"
#             "Would you like to be contacted in future", 
#             reply_markup=build_yes_or_no_keyboard()
#         )
#     except:
#         await message.answer(
#         text=f"Invalid email", 
#     )



async def send_survey_result(message: Message, data):
    text = markdown.text(
        "your survey results",
        "",
        markdown.text("Name:", markdown.hbold(data["full_name"])),
        markdown.text("Email:", markdown.hcode(data["email"])),
        (   "Cool"
            if data["newsletter_ok"] 
            else " And won't bother you again "
        ),
        sep="\n"
    )
    await message.answer(text=text,
                         reply_markup=ReplyKeyboardRemove())


@handler.message(Survey.email_news_later, F.text.casefold() == "yes")
async def handle_survey_email_newsletter_ok(message: Message, state: FSMContext):
    data = await state.update_data(newsletter_ok=True) 
    await state.clear()
    await send_survey_result(message, data)


@handler.message(Survey.email_news_later, F.text.casefold() == "no")
async def handle_survey_email_newsletter_not(message: Message, state: FSMContext):
    data = await state.update_data(newsletter_ok=False) 
    await state.clear() 
    await send_survey_result(message, data)


@handler.message(Survey.email_news_later)
async def handle_survey_email_newsletter_understand(message: Message):
    await message.answer("Sorry i didn't understand",
                         reply_markup=build_yes_or_no_keyboard()
                         )





