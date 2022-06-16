from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


main = types.InlineKeyboardMarkup(row_width=2)
#enroll_doc = types.InlineKeyboardMarkup(row_width=2)
#enroll_diag = types.InlineKeyboardMarkup(row_width=2)
#test_covid = types.InlineKeyboardMarkup(row_width=2)
#doc_at_home = types.InlineKeyboardMarkup(row_width=2)
#operator = types.InlineKeyboardMarkup(row_width=2)
#sale = types.InlineKeyboardMarkup(row_width=2)


#############################
cancel_board = types.InlineKeyboardMarkup(row_width=2)
cancel_board.add(
    InlineKeyboardButton(text="Главное меню", callback_data="main")
)
############################

main.add(
    InlineKeyboardButton(text="Диагностика", callback_data="menu_diagnostics"),
    InlineKeyboardButton(text="Лечение", callback_data="menu_heal"),
    InlineKeyboardButton(text="Восстановление", callback_data="menu_repair"),
    InlineKeyboardButton(text="Мои записи", callback_data="menu_mythreat"),
    InlineKeyboardButton(text="Консультация оператора ", url="https://t.me/moscow_clinic"),
    InlineKeyboardButton(text="Узнать об акциях клиники", url="https://moscowclinic.ru/offers")
    #InlineKeyboardButton(text="Запись к врачу", callback_data="enroll_doc"),
    #InlineKeyboardButton(text="Запись на диагностику", callback_data="enroll_diag"),
    #InlineKeyboardButton(text="Тестирование на COVID-19 ", callback_data="test_covid"),
    #InlineKeyboardButton(text="Вызвать врача на дом", callback_data="doc_at_home"),
    #InlineKeyboardButton(text="Узнать об акциях клиники", callback_data="sale")
)

#enroll_doc.add(
#    InlineKeyboardButton(text="Терапевт", callback_data="enroll_doc_terapevt"),
#    InlineKeyboardButton(text="Травматолог", callback_data="enroll_doc_travma"),
#    InlineKeyboardButton(text="Психиатр", callback_data="enroll_doc_psycho"),
#    InlineKeyboardButton(text="Уролог", callback_data="enroll_doc_urolog"),
#    InlineKeyboardButton(text="Гинеколог", callback_data="enroll_doc_ginekolog"),
#    InlineKeyboardButton(text="Главное меню", callback_data="main")
#)

#enroll_diag.add(
#    InlineKeyboardButton(text="МРТ", callback_data="enroll_doc_terapevt"),
#    InlineKeyboardButton(text="УЗИ", callback_data="enroll_doc_travma"),
#    InlineKeyboardButton(text="Рентген", callback_data="enroll_doc_psycho"),
#    InlineKeyboardButton(text="Гастроскопия", callback_data="enroll_doc_urolog"),
#    InlineKeyboardButton(text="Анализы", callback_data="enroll_doc_ginekolog"),
#    InlineKeyboardButton(text="Главное меню", callback_data="main")
#)

#test_covid.add(
#    types.InlineKeyboardButton(text="Cверхсрочный ПЦР-тест в клинике", callback_data="active_info"),
#    types.InlineKeyboardButton(text="Cрочный ПЦР-тест в клинике", callback_data="active_accept"),
#    types.InlineKeyboardButton(text="ПЦРТ-тест в клинике", callback_data="active_back"),
#    types.InlineKeyboardButton(text="Выезд медицинской сестры на дом", callback_data="active_back"),
#    InlineKeyboardButton(text="Главное меню", callback_data="main")
#)


#doc_at_home.add(
#    InlineKeyboardButton(text="Завтра", callback_data="doc_at_home_"),
#    InlineKeyboardButton(text="Завтра + 1 день", callback_data="doc_at_home_"),
#    InlineKeyboardButton(text="Завтра + 2 дня", callback_data="doc_at_home_"),
#    InlineKeyboardButton(text="Завтра + 3 дня", callback_data="doc_at_home_"),
#    InlineKeyboardButton(text="Главное меню", callback_data="main")
#)


##operator.add(
##    InlineKeyboardButton(text="Перейти в чат", url="https://t.me/moscow_clinic"),
##    InlineKeyboardButton(text="Главное меню", callback_data="main")
##)
##
##sale.add(
##    InlineKeyboardButton(text="Перейти на страницу с акциями", url="https://moscowclinic.ru/offers "),
##    InlineKeyboardButton(text="Главное меню", callback_data="main")
##)
