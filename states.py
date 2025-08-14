from aiogram.fsm.state import State, StatesGroup


class Promo(StatesGroup):
    enter_promo = State()


class TopUpBalance(StatesGroup):
    amount = State()
    token = State()
    network = State()