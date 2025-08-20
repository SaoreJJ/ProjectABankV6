import pytest
from datetime import datetime
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными транзакций"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:30:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-10T12:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-20T08:45:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2023-01-05T14:15:00.000000"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-25T18:20:00.000000"},
    ]


class TestFilterByState:
    """Тесты для функции filter_by_state"""

    def test_filter_executed(self, sample_transactions):
        """Тест фильтрации по статусу EXECUTED"""
        result = filter_by_state(sample_transactions)
        assert len(result) == 3
        assert all(t["state"] == "EXECUTED" for t in result)


class TestSortByDate:
    """Тесты для функции sort_by_date"""

    def test_sort_descending(self, sample_transactions):
        """Тест сортировки по убыванию (по умолчанию)"""
        result = sort_by_date(sample_transactions)
        assert [t["id"] for t in result] == [5, 3, 1, 2, 4]



@pytest.mark.parametrize("transactions, expected_ids", [
    ([], []),
    ([{"id": 1, "state": "EXECUTED", "date": "2023-01-01"}], [1]),
    ([
        {"id": 1, "state": "EXECUTED", "date": "2023-01-10"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-05"},
    ], [1, 2]),
])
def test_parametrized_sorting(transactions, expected_ids):
    """Параметризованный тест для функции сортировки"""
    result = sort_by_date(transactions)
    assert [t["id"] for t in result] == expected_ids