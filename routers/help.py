from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from loguru import logger

help_router = Router(name='help_router')

@help_router.message(Command('help'))
async def command_start(message: Message):
    logger.info('Обнаружена команда help')
    await message.answer('help')
    logger.info('Ответ отправлен!')