import logging
import os
from pathlib import Path


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """
    Настройка логгера для модуля

    Args:
        name: Имя логгера (обычно имя модуля)
        log_file: Имя файла для логов (например, 'masks.log')

    Returns:
        Настроенный логгер
    """
    # Создаем папку logs в корне проекта если ее нет
    project_root = Path(__file__).parent.parent  # Поднимаемся на уровень выше src
    log_dir = project_root / 'logs'
    log_dir.mkdir(exist_ok=True)

    # Полный путь к файлу лога в корне проекта
    log_path = log_dir / log_file

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Очищаем существующие обработчики (чтобы избежать дублирования)
    logger.handlers.clear()

    # Создаем файловый обработчик с ПЕРЕЗАПИСЬЮ при каждом запуске (mode='w')
    file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Форматтер для логов: время - модуль - уровень - сообщение
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger