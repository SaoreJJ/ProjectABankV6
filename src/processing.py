#from masks import get_mask_card_number  # закомментировано, пока не нужно
#from widget import mask_account_card, get_date  # закомментировано, пока не нужно

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

#data = [
#    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
#]


#print(sort_by_date(data))

#print(sort_by_date(data, reverse=False))
