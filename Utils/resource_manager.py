from __future__ import annotations
from dotenv import load_dotenv
from typing import final, Final
from pathlib import Path
from pydantic import BaseModel, field_validator, Field
from os import getenv
from re import match


@final
class Resources(BaseModel):
    """
    Получение ресурсов
    """
    # Константы
    DEFAULT_CONFIG_NAME: Final[str] = "Config.env"
    PATH_TO_CONFIG: Final[str] = Path(DEFAULT_CONFIG_NAME)

    # Базовые настройки окна
    token_key: str = Field(default=None, repr=True, init=True)

    @field_validator("token_key")
    @classmethod
    def validate_token(cls, value: str) -> str:
        # Паттерн для токена Telegram
        pattern = r'^\d+:[A-Za-z0-9_-]+$'

        if not match(pattern, value):
            raise ValueError("Некорректный формат токена")

        # Проверить длину второй части (обычно 35 символов)
        parts = value.split(':')
        if len(parts) != 2 or len(parts[1]) != 35:
            raise ValueError("Некорректная структура токена")

        return value

    @classmethod
    def from_config_file(cls, path_to_config_file: Path = PATH_TO_CONFIG) -> Resources:
        """Создать конфигурацию из файла"""
        try:
            load_dotenv(path_to_config_file)
            return cls(token_key=getenv('TOKEN'))
        except FileNotFoundError:
            return cls()
