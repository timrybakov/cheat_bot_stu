from aiogram.fsm.state import StatesGroup, State


class UserCallbackData(StatesGroup):
    start = State()
    academic_year = State()
    post = State()
    get = State()


class AdminCallbackData(StatesGroup):
    admin = State()
