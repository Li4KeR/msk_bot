from aiogram import types
from aiogram.types import InlineKeyboardButton


main = types.InlineKeyboardMarkup(row_width=2)

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
)
