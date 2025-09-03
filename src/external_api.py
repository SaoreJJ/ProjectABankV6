import os
import requests
from typing import Dict, Any, Optional, Union
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Сначала определяем типы, потом функции
from typing import TypedDict, NotRequired


class CurrencyInfo(TypedDict):
    """Тип для информации о валюте"""

    name: str
    code: str


class OperationAmount(TypedDict):
    """Тип для суммы операции"""

    amount: str
    currency: CurrencyInfo


class Transaction(TypedDict):
    """Тип для транзакции"""

    id: NotRequired[int]
    state: NotRequired[str]
    date: NotRequired[str]
    operationAmount: OperationAmount
    description: NotRequired[str]
    from_account: NotRequired[str]
    to: NotRequired[str]


def get_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях
    """
    try:
        # Проверяем наличие необходимых ключей
        operation_amount = transaction.get("operationAmount")
        if not operation_amount or not isinstance(operation_amount, dict):
            return 0.0

        amount_str = operation_amount.get("amount")
        currency_info = operation_amount.get("currency")

        if not amount_str or not currency_info or not isinstance(currency_info, dict):
            return 0.0

        currency_code = currency_info.get("code")
        if not currency_code:
            return 0.0

        amount = float(amount_str)

        if currency_code == "RUB":
            return amount

        if currency_code in ["USD", "EUR"]:
            exchange_rate = get_exchange_rate(currency_code, "RUB")
            return amount * exchange_rate

        return amount

    except (KeyError, ValueError, TypeError):
        return 0.0


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> float:
    """
    Получает текущий курс валюты через API
    """
    api_token: Optional[str] = os.getenv("API_LAYER_TOKEN")

    if not api_token:
        return 1.0

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={from_currency}&symbols={to_currency}"
    headers = {"apikey": api_token}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()

        rates = data.get("rates", {})
        if not isinstance(rates, dict):
            return 1.0

        exchange_rate = rates.get(to_currency)
        if exchange_rate is None:
            return 1.0

        return float(exchange_rate)

    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        return 1.0


def get_amount_in_rubles_strict(transaction: Transaction) -> float:
    """
    Строго типизированная версия функции
    """
    try:
        amount_str = transaction["operationAmount"]["amount"]
        currency_code = transaction["operationAmount"]["currency"]["code"]
        amount = float(amount_str)

        if currency_code == "RUB":
            return amount

        if currency_code in ["USD", "EUR"]:
            exchange_rate = get_exchange_rate(currency_code, "RUB")
            return amount * exchange_rate

        return amount

    except (KeyError, ValueError, TypeError):
        return 0.0
