from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте операции и возвращает итератор.

    :param transactions: Список словарей с транзакциями
    :param currency_code: Код валюты для фильтрации (например, "USD", "EUR", "RUB")
    :return: Итератор, выдающий транзакции с указанной валютой
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        if currency_info.get("code") == currency_code:
            yield transaction


from typing import Any, Dict, Iterator, List


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описание каждой транзакции по очереди.

    :param transactions: Список словарей с транзакциями
    :return: Итератор, выдающий описания транзакций
    """
    for transaction in transactions:
        description = transaction.get("description", "")
        yield description


from typing import Iterator


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    :param start: Начальный номер карты (от 1)
    :param end: Конечный номер карты (до 9999999999999999)
    :return: Итератор, выдающий номера карт в формате XXXX XXXX XXXX XXXX
    """
    if start < 1:
        raise ValueError("Начальный номер должен быть не менее 1")
    if end > 9999999999999999:
        raise ValueError("Конечный номер должен быть не более 9999999999999999")
    if start > end:
        raise ValueError("Начальный номер должен быть меньше или равен конечному")

    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями
        card_str = str(number).zfill(16)
        # Разбиваем на группы по 4 цифры
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted_card
