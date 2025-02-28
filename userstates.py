from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    encrypt_text = State()
    encrypt_key = State()

    decrypt_text = State()
    decrypt_key = State()