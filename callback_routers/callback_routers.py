from aiogram.types import CallbackQuery
from aiogram import F, Router
from loguru import logger

callback_routers = []
callback_router = Router(name='callback_button1')

@callback_router.callback_query(F.data == 'button1')
async def send_random_person(callback: CallbackQuery):
    logger.info('Нажата кнопка 1')
    await callback.message.answer('Нажата кнопка 1')
    await callback.answer()

@callback_router.callback_query(F.data == 'button2')
async def send_random_person(callback: CallbackQuery):
    logger.info('Нажата кнопка 2')
    await callback.message.answer('Нажата кнопка 2')
    await callback.answer()

