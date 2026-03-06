import asyncio
from Utils.resource_manager import Resources
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from Handlers.all_routers import all_routers


# Подгрузка из конфига
resources = Resources.from_files()
# Получение токена
TOKEN = resources.token
# Прикрепление бота к маршрутизатору
dp = Dispatcher()


async def main() -> None:
    # Инициализация бота
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    for router in all_routers:
        dp.include_router(router)
    # Старт прослушивания
    print('Всё ок бот слушает сообщения...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


