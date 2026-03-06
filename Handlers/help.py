from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

help_router = Router(name='help_router')

@help_router.message(Command('help'))
async def command_start(message: Message):
    await message.answer('help')