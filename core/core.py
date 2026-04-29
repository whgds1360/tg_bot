from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkApi
from utils.resource_manager import Resources


class Core:

    @classmethod
    def __load_main_requirements(cls):
        # Подгрузка конфига
        cls.resources = Resources.load_config()
        logger.debug("Конфигурацию загружена успешно!")

    @classmethod
    def __initialization_tg_bot(cls):
        cls.bot = Bot(token=cls.resources.TG_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        cls.dp = Dispatcher()
        logger.debug("Инициализация тг бота успешна!")

    @classmethod
    def __initialization_vk_session(cls):
        cls.vk_session = VkApi(token=cls.resources.VK_TOKEN)
        cls.vk = cls.vk_session.get_api()
        logger.debug("Инициализация сессии успешна!")

    @classmethod
    async def __vk_listener(cls):

        logger.info(f"ВК токен:{cls.resources.VK_TOKEN}\nТГ токен:{cls.resources.TG_BOT_TOKEN}")

        longpoll = VkBotLongPoll(vk=cls.vk_session, group_id=cls.resources.VK_COMMUNITY_TOKEN)
        logger.info("VK Long Poll запущен")

        list_of_listen = map(int, cls.resources.LIST_OF_LISTEN.split(","))

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.obj.message
                text = msg.get('text', '')
                peer_id = msg.get('peer_id')

                if text and peer_id in list_of_listen:
                    # Получение имени отправителя
                    try:
                        user = cls.vk.users.get(user_ids=msg['from_id'])[0]
                        name = f"{user['first_name']} {user['last_name']}"
                    except KeyError:
                        name = f"id{msg['from_id']}"
                        logger.exception(f"Ошибка с получением имени отправителя")

                    await cls.bot.send_message(
                        chat_id=cls.resources.CHAT_ID,
                        text=f"💬 {name}:\n{text}"
                    )
                    logger.debug(f"Переслано из беседы {peer_id}:\n{text[:20]}")

                else:
                    logger.error(f"Ошибка мы смотрим на такое ID чата {peer_id} в таком списке просмотра {list(list_of_listen)}")
                    logger.info(f"Из конфига пришло: {cls.resources.LIST_OF_LISTEN}")

    @classmethod
    async def main(cls):
        cls.__load_main_requirements()
        cls.__initialization_tg_bot()
        cls.__initialization_vk_session()
        await cls.__vk_listener()
        logger.info("Запуск Telegram бота...")
