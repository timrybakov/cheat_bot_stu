from aiogram.fsm.state import StatesGroup, State


class UserCallbackData(StatesGroup):
    start_conversation_state = State()
    choosing_academic_year_state = State()
    posting_data_state = State()
    getting_data_state = State()
