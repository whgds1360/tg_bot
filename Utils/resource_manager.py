from __future__ import annotations
from pathlib import Path
from typing import Final, final, Dict, Optional
from dotenv import load_dotenv
from os import getenv
from re import match
from pydantic import BaseModel, field_validator, Field, ConfigDict
from json import load
from loguru import logger


@final
class Resources(BaseModel):
    """
    Конфигурация бота: токен + тексты сообщений
    """
    model_config = ConfigDict(
        extra='ignore',           # Если передаем лишние поля их игнорим
        frozen=True,              # После создания экземпляра его нельзя изменять
        validate_default=False,    # Проводим валидацию для дефолтных значений
    )

    # Константы
    DEFAULT_ENV_FILE: Final[Path] = Path("config.env")
    DEFAULT_TEXT_FILE: Final[Path] = Path("text_config.json")

    token: Optional[str] = Field(default=None, repr=False)

    start_text: Optional[str] = Field(default=None, repr=False)
    help_text:  Optional[str] = Field(default=None, repr=False)
    menu_text:  Optional[str] = Field(default=None, repr=False)

    @field_validator("token", mode='before')
    @classmethod
    def validate_token(cls, value: str | None) -> str:
        if not value:
            raise ValueError("Токен бота не указан")

        pattern = r'^\d+:[A-Za-z0-9_-]{35}$'
        if not match(pattern, value):
            raise ValueError(
                "Некорректный формат токена. Ожидается: числа: 35символов_из_букв_цифр_и_подчёркиваний"
            )

        return value

    @staticmethod
    def __load_json(text_path: Optional[Path]) -> Optional[Dict[str, str]]:
        """
        Загрузка текста из json
        """
        texts = None
        if text_path.exists():
            try:
                with text_path.open("r", encoding="utf-8") as f:
                    texts = load(f)  # json.load → dict
            except Exception as e:
                logger.warning(f"Ошибка чтения текстов: {text_path} - {e}")
        else:
            logger.warning(f"Предупреждение: файл с текстами не найден - {text_path}")

        return texts

    @staticmethod
    def __load_text(env_path: Optional[Path]) -> None:
        """
        Загрузка из env
        """
        if env_path.exists():
            load_dotenv(env_path)
        else:
            logger.warning("Предупреждение: файл окружения не найден")

    @classmethod
    def from_files(cls, env_path: Optional[Path] = None, text_path: Optional[Path] = None) -> Resources:
        """
        Загружает конфигурацию из .env и json-файла с текстами
        """
        env_path = env_path or cls.DEFAULT_ENV_FILE
        text_path = text_path or cls.DEFAULT_TEXT_FILE

        # Получение токена
        cls.__load_text(env_path=env_path)
        token = getenv("TOKEN").strip()

        # Получение текстов
        texts = cls.__load_json(text_path=text_path)

        # Формируем словарь для Pydantic
        data = {
            "token": token,
            "start_text": texts.get("start", None),
            "help_text":  texts.get("help",  None),
            "menu_text":  texts.get("menu",  None),
        }

        try:
            return cls.model_validate(data)
        except AttributeError:
            return cls()
