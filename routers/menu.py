from loguru import logger
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboard.keyboard import main_menu


menu_router = Router(name='menu_router')

@menu_router.message(Command('menu'))
async def command_menu(message: Message):
    logger.info('Обнаружена команда menu')
    await message.answer('menu', reply_markup=main_menu())
    logger.info('Ответ отправлен!')
