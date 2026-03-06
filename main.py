import asyncio
from Utils.resource_manager import Resources
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Подгрузка из конфига
resources = Resources.from_config_file()
# Получение токена
TOKEN = resources.token_key
# Прикрепление бота к маршрутизатору
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    # Инициализация бота
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # Старт прослушивания
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

