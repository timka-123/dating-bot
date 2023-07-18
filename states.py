from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    ENTER_NAME = State()
    ENTER_AGE = State()
    ENTER_CITY = State()
    ENTER_INFO = State()
    SEARCH_PEOPLE = State()
    UPLOAD_PHOTO = State()
