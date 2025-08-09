# Проект "CardBank"

## Описание:

Этот проект предоставляет инструменты для обработки банковских транзакций:

- Фильтрация по статусу (EXECUTED, CANCELED и др.).

- Сортировка по дате (по возрастанию/убыванию).

- Маскировка номеров карт и счетов (1234 56** **** 3456, Счет **1234).

Используется для анализа банковских операций, логирования транзакций и защиты конфиденциальных данных.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/SaoreJJ/card_bankO.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:

1. Фильтрация транзакций (filter_by_state)
Возвращает транзакции с указанным статусом (EXECUTED по умолчанию).

Пример:
```
from processing import filter_by_state

transactions = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01'},
    {'id': 2, 'state': 'CANCELED', 'date': '2023-01-02'}
]

# Фильтрация по статусу 'EXECUTED'
executed_transactions = filter_by_state(transactions)
print(executed_transactions)  
# [{'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01'}]
```
2. Сортировка по дате (sort_by_date)
Сортирует транзакции по дате (новые → старые по умолчанию).

Пример:
```
from processing import sort_by_date

sorted_transactions = sort_by_date(transactions)
print(sorted_transactions)  
# [{'id': 2, 'state': 'CANCELED', 'date': '2023-01-02'}, {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01'}]
```
3. Маскировка данных (из masks.py и widget.py)
get_mask_card_number("1234567890123456") → "1234 56** **** 3456"

mask_account_card("Счет 12345678") → "Счет **5678"

Пример:
```
from masks import get_mask_card_number
from widget import mask_account_card

print(get_mask_card_number("1234567890123456"))  # 1234 56** **** 3456
print(mask_account_card("Счет 12345678"))       # Счет **5678
```

