import os
import sys
from typing import List, Dict, Any
from datetime import datetime

# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils import load_transactions
from src.pandas_utils import read_transactions_from_csv, read_transactions_from_excel
from src.processing import filter_by_state, sort_by_date, filter_by_description, count_operations_by_category
from src.external_api import get_amount_in_rubles
from src.widget import mask_account_card, get_date
from src.masks import get_mask_account, get_mask_card_number


def print_transaction(transaction: Dict[str, Any]) -> None:
    """Печатает информацию о транзакции в читаемом формате"""
    if not transaction:
        return

    # Дата
    date_str = get_date(transaction.get("date", "")) if transaction.get("date") else "Дата неизвестна"

    # Описание
    description = transaction.get("description", "Описание отсутствует")

    # Откуда и куда
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    # Маскировка счетов/карт
    if from_account:
        from_account = mask_account_card(from_account)
    if to_account:
        to_account = mask_account_card(to_account)

    # Сумма в рублях
    amount_rub = get_amount_in_rubles(transaction)

    print(f"{date_str} {description}")
    if from_account and to_account:
        print(f"{from_account} -> {to_account}")
    elif from_account:
        print(f"{from_account}")
    elif to_account:
        print(f"-> {to_account}")

    print(f"Сумма: {amount_rub:.2f} руб.")
    print()


def get_user_input(prompt: str, valid_options: List[str] = None) -> str:
    """Получает ввод от пользователя с валидацией"""
    while True:
        user_input = input(prompt).strip().lower()

        if not valid_options:
            return user_input

        if user_input in [opt.lower() for opt in valid_options]:
            return user_input

        print(f"Неверный ввод. Допустимые варианты: {', '.join(valid_options)}")


def main() -> None:
    """Основная функция программы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = get_user_input("Ваш выбор (1-3): ", ["1", "2", "3"])

    transactions = []
    file_type = ""

    if choice == "1":
        file_type = "JSON"
        file_path = input("Введите путь к JSON-файлу: ").strip()
        transactions = load_transactions(file_path)
    elif choice == "2":
        file_type = "CSV"
        file_path = input("Введите путь к CSV-файлу: ").strip()
        transactions = read_transactions_from_csv(file_path)
    elif choice == "3":
        file_type = "XLSX"
        file_path = input("Введите путь к XLSX-файлу: ").strip()
        transactions = read_transactions_from_excel(file_path)

    print(f"Для обработки выбран {file_type}-файл.")
    print(f"Загружено {len(transactions)} транзакций.")

    if not transactions:
        print("Не удалось загрузить транзакции. Программа завершена.")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")

        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            filtered_transactions = filter_by_state(transactions, status)
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            break
        else:
            print(f"Статус операции \"{status}\" недоступен.")

    # Сортировка по дате
    sort_choice = get_user_input("Отсортировать операции по дате? (да/нет): ", ["да", "нет"])

    if sort_choice == "да":
        sort_direction = get_user_input("Отсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию): ",
                                        ["по возрастанию", "по убыванию"])

        reverse = sort_direction == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, reverse)
        print(f"Операции отсортированы {sort_direction}")

    # Фильтрация по валюте
    currency_choice = get_user_input("Выводить только рублевые транзакции? (да/нет): ", ["да", "нет"])

    if currency_choice == "да":
        filtered_transactions = [t for t in filtered_transactions
                                 if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]
        print("Оставлены только рублевые транзакции")

    # Фильтрация по описанию
    search_choice = get_user_input("Отфильтровать список транзакций по определенному слову в описании? (да/нет): ",
                                   ["да", "нет"])

    if search_choice == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered_transactions = filter_by_description(filtered_transactions, search_word)
            print(f"Отфильтровано по слову \"{search_word}\"")

    # Вывод результатов
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    for transaction in filtered_transactions:
        print_transaction(transaction)

    # Дополнительная статистика
    stats_choice = get_user_input("Показать статистику по категориям операций? (да/нет): ", ["да", "нет"])

    if stats_choice == "да":
        common_categories = ["перевод", "оплата", "вклад", "покупка", "снятие"]
        category_stats = count_operations_by_category(filtered_transactions, common_categories)

        print("\nСтатистика по категориям операций:")
        for category, count in category_stats.items():
            if count > 0:
                print(f"{category.capitalize()}: {count} операций")


if __name__ == "__main__":
    main()