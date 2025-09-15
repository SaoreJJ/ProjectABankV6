# from masks import get_mask_card_number  # закомментировано, пока не нужно
# from widget import mask_account_card, get_date  # закомментировано, пока не нужно

import re
from typing import List, Dict, Any
from collections import Counter


def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param transactions: Список словарей для фильтрации
    :param state: Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED')
    :return: Отфильтрованный список словарей
    """
    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате (ключ 'date').

    :param transactions: Список словарей для сортировки.
    :param reverse: Если True (по умолчанию), сортировка по убыванию (новые сначала).
                   Если False, сортировка по возрастанию (старые сначала).
    :return: Новый список словарей, отсортированный по дате.
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)


def filter_by_description(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по строке поиска в описании с использованием регулярных выражений.

    Args:
        data: Список словарей с транзакциями
        search: Строка для поиска в описании (регистронезависимо)

    Returns:
        Отфильтрованный список транзакций

    Raises:
        re.error: Если переданное регулярное выражение некорректно
    """
    if not search:
        return data

    try:
        pattern = re.compile(search, re.IGNORECASE)
        return [
            transaction for transaction in data
            if transaction.get("description") and pattern.search(transaction["description"])
        ]
    except re.error as e:
        raise re.error(f"Некорректное регулярное выражение '{search}': {e}")


def count_operations_by_category(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям с использованием Counter.

    Args:
        data: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством операций по каждой категории
    """
    category_counter = Counter()

    for transaction in data:
        description = transaction.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                category_counter[category] += 1
                break

    # Создаем словарь с нулевыми значениями для всех категорий
    result = {category: 0 for category in categories}
    result.update(category_counter)  # Обновляем реальными значениями

    return result

# Тестовые данные (закомментированы)
# data = [
#     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
# ]