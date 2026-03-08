from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кнопка 1", callback_data="button1")],
        [InlineKeyboardButton(text="Кнопка 2", callback_data="button2")]
        ])
    return keyboard

