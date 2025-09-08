from typing import Union
import os
import sys

# Добавляем путь к src для импорта config
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
        masks_logger.info(f"Начало обработки номера карты: {card_number}")
        str_number = str(card_number).strip()

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
        masks_logger.info(f"Начало обработки номера счета: {account_number}")
        str_number = str(account_number).strip()

        if not str_number.isdigit():
            error_msg = "Номер счёта должен содержать только цифры"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        if len(str_number) < 4:
            error_msg = "Номер счёта должен содержать минимум 4 цифры"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        result = f"**{str_number[-4:]}"
        masks_logger.info(f"Успешно замаскирован номер счета: {result}")
        return result

    except Exception as e:
        masks_logger.exception(f"Ошибка при маскировании номера счета: {e}")
        raise


# Пример использования
if __name__ == "__main__":
    try:
        print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361
        print(get_mask_card_number(4111111111111111))  # 4111 11** **** 1111
        print(get_mask_account("73654108430135874305"))  # **4305
        print(get_mask_account("1234567890"))  # **7890
        print(get_mask_account(1234))  # **1234

    except Exception as e:
        print(f"Произошла ошибка: {e}")