from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX
    :param card_number: Номер карты (строка или число)
    :return: Маскированный номер карты
    """
    str_number = str(card_number).strip()
    # Преобразуем в строку на случай, если передано число
    str_number = str(card_number).strip()
    # Проверяем, что номер состоит только из цифр
    if not str_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    # Проверяем длину номера (стандартно 16 цифр)
    if len(str_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    # Форматируем номер: первые 6 и последние 4 цифры видимы, остальное — звёздочки
    masked = f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"
    return masked


# Пример использования
print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361
print(get_mask_card_number(4111111111111111))  # 4111 11** **** 1111


def get_mask_account(account_number: Union[str, int]) -> str:
    """
    Маскирует номер счёта, оставляя только последние 4 цифры.
    Формат: **XXXX, где X — последние 4 цифры номера счёта.

    :param account_number: Номер счёта (строка или число)
    :return: Маскированный номер счёта (формат **XXXX)
    """
    str_number = str(account_number).strip()
    str_number = str(account_number).strip()

    if not str_number.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")

    if len(str_number) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    return f"**{str_number[-4:]}"


# Примеры использования
print(get_mask_account("73654108430135874305"))  # **4305
print(get_mask_account("1234567890"))  # **7890
print(get_mask_account(1234))  # **1234
