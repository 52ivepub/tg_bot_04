# from enum import E
from enum import Enum
from aiogram.fsm.state import State, StatesGroup


class Survey(StatesGroup):
    full_name = State()
    email = State()
    sport = State()
    email_news_later = State()


class SportDetails(StatesGroup):
    tennis = State()
    footbal = State()
    formaule_one = State()
    


class KnowSports(str, Enum):
    tennis = "Tennis"
    footbal = "Footbal"
    formaule_one = "Formaule_one"


class KnowF1Tracks(str, Enum):
    monako = "Monako"
    spa = "Spa"
    suzuka = "Suzuka"
    monza = "Monza"