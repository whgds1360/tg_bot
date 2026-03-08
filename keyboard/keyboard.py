from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать временную почту", callback_data="button1")],
        [InlineKeyboardButton(text="Получить ключ", callback_data="button2")],
        [InlineKeyboardButton(text="Настройки", callback_data="button3")],
        [InlineKeyboardButton(text="Кинуть кубик", callback_data="button4")],
        ])
    return keyboard

