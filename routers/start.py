from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger


start_router = Router(name='start_router')

@start_router.message(Command('start'))
async def command_start(message: Message):
    logger.info('Обнаружена команда start')
    await message.answer('start')
    logger.info('Ответ отправлен!')