from loguru import logger
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
    # Включения роутеров
    for router in all_routers:
        dp.include_router(router)
    # Старт прослушивания
    logger.info('Запуск бота ...')
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Остановка по Ctrl+C")
    except Exception as e:
        logger.exception("Ошибка polling: ", e)
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())


