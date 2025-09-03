from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}, "description": "Перевод"},
        {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "EUR"}}, "description": "Оплата"},
        {"id": 3, "operationAmount": {"amount": "300", "currency": {"code": "USD"}}},
    ]


def test_filter_by_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    usd = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd)


def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    desc = list(transaction_descriptions(sample_transactions))
    assert desc == ["Перевод", "Оплата", ""]


@pytest.mark.parametrize("start,end,expected", [
    (1, 1, ["0000 0000 0000 0001"]),
    (9999, 10000, ["0000 0000 0000 9999", "0000 0000 0001 0000"]),
])
def test_card_number_generator(start: int, end: int, expected: List[str]) -> None:
    assert list(card_number_generator(start, end)) == expected
