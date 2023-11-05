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
    enter_event_date = State()
    enter_count_of_event_normal = State()
    enter_count_of_event_deposit = State()
    enter_prices_range = State()
    continue_to_prices_range = State()
    saving_or_editing_from_the_beginning = State()

    upload_data = State()
    upload_data_in_format = State()
    upload_data_in_format_final = State()

    ticket_refund = State()
    choose_event_to_refund = State()
    enter_ticket_type_to_refund = State()
    enter_ticket_number = State()
    approve_ticket_refund = State()

    enter_event_name_for_ticket_addition = State()
    enter_ticket_type_for_addition = State()
    enter_number_of_tickets_for_addition = State()
    enter_count_of_event_normal_for_addition = State()
    enter_count_of_event_prime_for_addition = State()
    confirm_event_addition_tickets = State()
    confirm_ticket_addition = State()

    choose_event_to_change_price_range = State()
    enter_price_range_for_change = State()
    saving_or_editing_from_the_beginning_price_range = State()

    choose_event_to_show = State()
    choose_action_to_show_or_hide = State()

    begin_mailing = State()
    mailing_with_text = State()
    mailing_with_photo = State()
    mailing_with_file = State()



class PromouterStates(StatesGroup):
    main = State()
    begin_registration = State()
    enter_initials = State()
    enter_number = State()
    waitng_for_admin_accept = State()
    accepted_promouter_panel = State()
    main_accepted_promouter_panel = State()
    choose_event_for_participants_registration = State()
    enter_personal_data_of_participant = State()
    enter_participant_gender = State()
    enter_education_program_of_participant = State()
    enter_ticket_type = State()
    enter_price = State()
    confirm_participant = State()
    choose_event_for_participants_refund = State()
    choose_ticket_type_for_refund = State()
    enter_number_of_ticket_for_refund = State()
    confirm_ticket_data_for_refund = State()
    get_admin_confirmation_to_refund = State()
    choose_event_for_info = State()
    tickets_info_final = State()