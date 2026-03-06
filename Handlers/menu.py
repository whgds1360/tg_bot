from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


menu_router = Router(name='menu_router')

@menu_router.message(Command('menu'))
async def command_menu(message: Message):
    await message.answer('menu')