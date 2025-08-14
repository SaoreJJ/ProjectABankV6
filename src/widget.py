from masks import get_mask_account, get_mask_card_number


def mask_account_card(input_str: str) -> str:
    """
    Маскирует номер карты/счета в строке формата "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"
    Возвращает строку с сохранением названия и маскированным номером
    """
    if "счет" in input_str.lower():
        # Обработка счета
        parts = input_str.split()
        return f"{' '.join(parts[:-1])} {get_mask_account(parts[-1])}"
    else:
        # Обработка карты
        parts = input_str.split()
        return f"{' '.join(parts[:-1])} {get_mask_card_number(parts[-1])}"


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата '2018-07-11T02:26:18.671407' в '11.07.2018'
    """
    from datetime import datetime

    dt = datetime.strptime(date_str.split("T")[0], "%Y-%m-%d")
    return dt.strftime("%d.%m.%Y")


# Примеры использования
print(mask_account_card("Visa Platinum 7000792289606361")) # Visa Platinum 7000 79** **** 6361
print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305
print(get_date("2018-07-11T02:26:18.671407"))  # 11.07.2018
