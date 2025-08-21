from aiogram.fsm.state import StatesGroup, State


class OrderFoodStates(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


class CalculatorStates(StatesGroup):
    choosing_first_number = State()
    choosing_second_number = State()
    choosing_operation = State()


class VoteIns(StatesGroup):
    send_phone = State()
    send_submit_code = State()