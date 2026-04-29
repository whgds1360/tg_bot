from __future__ import annotations
from pathlib import Path
from typing import Final, final
from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel, Field, ConfigDict
from loguru import logger


@final
class Resources(BaseModel):
    """
    Класс управления ресурсами
    """
    model_config = ConfigDict(
        extra='ignore',
        frozen=True,
        validate_default=True,
    )

    # Константы
    DEFAULT_ENV_FILE: Final[Path] = Path("config.env")

    TG_BOT_TOKEN: str = Field(default="", init=True, repr=False)
    LIST_OF_LISTEN: str = Field(default="", init=True, repr=False)
    VK_TOKEN: str = Field(default="", init=True, repr=False)
    VK_COMMUNITY_TOKEN: str = Field(default="", init=True, repr=False)
    CHAT_ID: str = Field(default="", init=True, repr=False)

    @staticmethod
    def __load_env_config(env_path: Path) -> None:
        """
        Подгрузка переменных из env в код
        """
        if env_path.exists():
            load_dotenv(env_path)
        else:
            logger.warning("Предупреждение: файл окружения не найден")

    @classmethod
    def load_config(cls, env_path: Path = None) -> Resources:
        """
        Загружает конфигурацию из .env
        """
        env_path = env_path or cls.DEFAULT_ENV_FILE

        cls.__load_env_config(env_path=env_path)

        tg_bot_token = getenv("TG_BOT_TOKEN")
        list_of_listen = getenv("LIST_OF_LISTEN")
        vk_token = getenv("VK_TOKEN")
        vk_community_token = getenv("VK_COMMUNITY_TOKEN")
        chat_id = getenv("CHAT_ID")

        data = {
            "TG_BOT_TOKEN": tg_bot_token,
            "LIST_OF_LISTEN": list_of_listen,
            "VK_TOKEN":  vk_token,
            "VK_COMMUNITY_TOKEN": vk_community_token,
            "CHAT_ID": chat_id
                }

        try:
            return cls.model_validate(data)
        except AttributeError:
            return cls()
