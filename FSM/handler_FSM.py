from FSM.states import KnowF1Tracks, KnowSports, SportDetails, Survey
import email
import logging
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, any_state, default_state
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils import markdown
from email_validator import validate_email, EmailNotValidError


from FSM.keyboard_FSM import build_select_keyboard, build_yes_or_no_keyboard, valid_email_filter, valid_email, valid_email_message_text

handler_FSM = Router()


@handler_FSM.message(Command('survey'), default_state)
async def handle_start(message: Message, state: FSMContext):
    await state.set_state(Survey.full_name)
    await message.answer(
        text="Welcome to our weekly survey, Whats your name ?",
        reply_markup=ReplyKeyboardRemove(),
    )


@handler_FSM.message(Command("cancel"), StateFilter(Survey(), SportDetails()))
@handler_FSM.message(F.text.casefold() == "cancel", StateFilter(Survey(), SportDetails()))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    logging.info("Canceling survey %r", current_state)
    await state.clear()
    await message.answer(
        text=f"Cancelled survey state {current_state} start again /survey",
        reply_markup=ReplyKeyboardRemove(),
    )


# ==================FULL_NAME===================================
@handler_FSM.message(Survey.full_name, F.text)
async def handler_survey_user_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(Survey.email)
    await message.answer(
        f"Hello {markdown.hbold(message.text)}, now please share your email",
        parse_mode=ParseMode.HTML,
                
    )

@handler_FSM.message(Survey.full_name)
async def handle_survey_user_full_name_invalid_content_type(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Sorry, I didn't understand, send your full name as text"
    )

# ==========================================================================


# ==================EMAIL===================================
@handler_FSM.message(
        Survey.email,
        F.text.cast(validate_email).normalized.as_("email"),
        # F.text.cast(valid_email).normalized.as_("email"),   # МОЖНО ТАК
        # F.func(valid_email_message_text).as_("email")       # МОЖНО И  ТАК
        )
async def handler_survey_user_email(
    message: Message,
    state: FSMContext,
    email: str):
    await state.update_data(email=message.text)
    await state.set_state(Survey.sport)
    await message.answer(
        text=f"Cool yuor email is now {markdown.hcode(email)}\n"
        "Which sport would your prefer ?", 
        reply_markup=build_select_keyboard(KnowSports),
    )


@handler_FSM.message(Survey.email)
async def handler_survey_invalid_email(
    message: Message):
    await message.answer(
        text=f"Invalid email. Cancel survey, Tab /cancel", 
    )
# ==========================================================================

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


# ==================EMAIL_NEWS_LATER===================================
@handler_FSM.message(Survey.email_news_later, F.text.casefold() == "yes")
async def handle_survey_email_newsletter_ok(message: Message, state: FSMContext):
    data = await state.update_data(newsletter_ok=True) 
    await state.clear()
    await send_survey_result(message, data)


@handler_FSM.message(Survey.email_news_later, F.text.casefold() == "no")
async def handle_survey_email_newsletter_not(message: Message, state: FSMContext):
    data = await state.update_data(newsletter_ok=False) 
    await state.clear() 
    await send_survey_result(message, data)


@handler_FSM.message(Survey.email_news_later)
async def handle_survey_email_newsletter_understand(message: Message):
    await message.answer("Sorry i didn't understand",
                         reply_markup=build_yes_or_no_keyboard()
                         )
# ==========================================================================


# ==================SPORT===================================
know_sport_to_next: dict[KnowSports, tuple[State, str]] = {
    KnowSports.tennis: (
        SportDetails.tennis,
        "Who is your favorite tennis player ?"
    ),
    KnowSports.footbal: (
        SportDetails.footbal,
        "What is your favorite footbal team ?"
    ),
    KnowSports.formaule_one: (
        SportDetails.formaule_one,
        "What is your favorite formula track ?"
    ),
}

know_sport_to_kb: dict = {
    KnowSports.formaule_one: build_select_keyboard(KnowF1Tracks),
}

@handler_FSM.message(Survey.sport, F.text.cast(KnowSports),
        )
async def select_sport(message: Message, state: FSMContext):
    await state.update_data(sport=message.text)
    next_state, question_text = know_sport_to_next[message.text]
    await state.set_state(next_state)
    kb = ReplyKeyboardRemove()
    if message.text in know_sport_to_kb:
        kb = know_sport_to_kb[message.text]
    await message.answer(
        text=question_text,
        reply_markup=kb,
    )
 


@handler_FSM.message(Survey.sport)
async def select_sport_invalid_choice(message: Message):
    await message.answer(
        text="Unknown sport, please select one of the following:",
        reply_markup=build_select_keyboard(KnowSports),
    )


@handler_FSM.message(F.text,
                    StateFilter(SportDetails.tennis, SportDetails.footbal),
                     )
async def handle_selected_sport_details_option(
        message: Message,
        state: FSMContext):
    await state.update_data(sport_details=message.text)




# ==========================================================================







