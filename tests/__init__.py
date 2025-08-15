import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card

# Корректное добавление пути к src (после всех импортов)
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def test_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными транзакций."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:30:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-10T12:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-20T08:45:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2023-01-05T14:15:00.000000"},
    ]


def test_card_masking() -> None:
    """Тест маскировки номеров карт."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"


def test_account_card_formatting() -> None:
    """Тест форматирования карт/счетов."""
    result = mask_account_card("Visa Platinum 7000792289606361")
    assert result == "Visa Platinum 7000 79** **** 6361"


def test_empty_data_handling() -> None:
    """Тест обработки пустых данных."""
    assert filter_by_state([]) == []