import sys
from pathlib import Path
from typing import List, Dict, Any
import pytest

# Корректное добавление пути к src
sys.path.insert(0, str(Path(__file__).parent.parent))

# Абсолютные импорты из src
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


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


def test_account_masking() -> None:
    """Тест маскировки номеров счетов."""
    assert get_mask_account("73654108430135874305") == "**4305"
    assert get_mask_account("12345678901234567890") == "**7890"


def test_state_filtering(test_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по состоянию."""
    executed = filter_by_state(test_transactions)
    assert len(executed) == 2
    assert executed[0]["id"] == 1

    canceled = filter_by_state(test_transactions, "CANCELED")
    assert len(canceled) == 1
    assert canceled[0]["id"] == 2



def test_invalid_account_numbers() -> None:
    """Тест невалидных номеров счетов."""
    with pytest.raises(ValueError):
        get_mask_account("123")


