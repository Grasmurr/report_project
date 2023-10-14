from aiogram.fsm.state import StatesGroup, State


class MainMenuStates(StatesGroup):
    report_choose = State()


class AdminStates(StatesGroup):
    main = State()
    manage_events = State()
    enter_event_name = State()
    delete_event = State()
    confirm_event_name = State()
    enter_count_of_event_prime = State()
    enter_count_of_event_normal = State()
    saving_or_editing_from_the_beginning = State()
    ticket_refund = State()
    upload_data = State()
    upload_data_in_format = State()
    upload_data_in_format_final = State()

class PromouterStates(StatesGroup):
    main = State()
    main_enter_data = State()
    main_enter_telephone = State()
    main_enter_course = State()
