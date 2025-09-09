from typing import Union
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import setup_logger

# Настройка логгера
masks_logger = setup_logger('masks', 'masks.log')


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX
    :param card_number: Номер карты (строка или число)
    :return: Маскированный номер карты
    """
    try:
        masks_logger.debug(f"Получен номер карты для маскирования: {card_number}")
        masks_logger.info(f"Начало обработки номера карты: {card_number}")
        str_number = str(card_number).strip()
        masks_logger.debug(f"Номер после очистки: {str_number}")

        # Проверяем, что номер состоит только из цифр
        if not str_number.isdigit():
            error_msg = "Номер карты должен содержать только цифры"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Проверяем длину номера (стандартно 16 цифр)
        if len(str_number) != 16:
            error_msg = "Номер карты должен содержать 16 цифр"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Форматируем номер: первые 6 и последние 4 цифры видимы, остальное — звёздочки
        masked = f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"
        masks_logger.debug(f"Результат маскирования: {masked}")
        masks_logger.info(f"Успешно замаскирован номер карты: {masked}")
        return masked

    except Exception as e:
        masks_logger.exception(f"Ошибка при маскировании номера карты: {e}")
        raise


def get_mask_account(account_number: Union[str, int]) -> str:
    """
    Маскирует номер счёта, оставляя только последние 4 цифры.
    Формат: **XXXX, где X — последние 4 цифры номера счёта.

    :param account_number: Номер счёта (строка или число)
    :return: Маскированный номер счёта (формат **XXXX)
    """
    try:
        masks_logger.debug(f"Получен номер счета для маскирования: {account_number}")
        masks_logger.info(f"Начало обработки номера счета: {account_number}")
        str_number = str(account_number).strip()
        masks_logger.debug(f"Номер после очистки: {str_number}")

        if not str_number.isdigit():
            error_msg = "Номер счёта должен содержать только цифры"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        if len(str_number) < 4:
            error_msg = "Номер счёта должен содержать минимум 4 цифры"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        result = f"**{str_number[-4:]}"
        masks_logger.debug(f"Результат маскирования счета: {result}")
        masks_logger.info(f"Успешно замаскирован номер счета: {result}")
        return result

    except Exception as e:
        masks_logger.exception(f"Ошибка при маскировании номера счета: {e}")
        raise