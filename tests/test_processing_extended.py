import pytest
import re
from typing import List, Dict, Any
from src.processing import filter_by_description, count_operations_by_category


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "description": "Перевод организации", "amount": 100},
        {"id": 2, "description": "Оплата услуг", "amount": 200},
        {"id": 3, "description": "Открытие вклада", "amount": 300},
        {"id": 4, "description": "Покупка в магазине", "amount": 400},
        {"id": 5, "description": "Снятие наличных", "amount": 500},
        {"id": 6, "description": "Другая операция", "amount": 600},  # Без категории
    ]


def test_filter_by_description(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по описанию с регулярными выражениями"""
    # Поиск точного слова
    result = filter_by_description(sample_transactions, "перевод")
    assert len(result) == 1
    assert result[0]["id"] == 1

    # Поиск с регистронезависимостью
    result = filter_by_description(sample_transactions, "ОПЛАТА")
    assert len(result) == 1
    assert result[0]["id"] == 2

    # Поиск части слова
    result = filter_by_description(sample_transactions, "вклад")
    assert len(result) == 1
    assert result[0]["id"] == 3


def test_filter_by_description_no_match(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации когда нет совпадений"""
    result = filter_by_description(sample_transactions, "несуществующееслово")
    assert len(result) == 0


def test_filter_by_description_empty_search(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации с пустой строкой поиска"""
    result = filter_by_description(sample_transactions, "")
    assert len(result) == 6  # Все транзакции должны вернуться


def test_filter_by_description_invalid_regex() -> None:
    """Тест обработки некорректного регулярного выражения"""
    transactions = [{"id": 1, "description": "test", "amount": 100}]

    with pytest.raises(re.error):
        filter_by_description(transactions, "[invalid-regex")


def test_count_operations_by_category(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест подсчета операций по категориям с Counter"""
    categories = ["перевод", "оплата", "вклад", "покупка", "снятие"]

    result = count_operations_by_category(sample_transactions, categories)

    assert result["перевод"] == 1
    assert result["оплата"] == 1
    assert result["вклад"] == 1
    assert result["покупка"] == 1
    assert result["снятие"] == 1

    # Проверяем что все категории присутствуют, даже с нулевыми значениями
    assert all(category in result for category in categories)


def test_count_operations_by_category_partial(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест подсчета с частичным списком категорий"""
    categories = ["перевод", "вклад"]

    result = count_operations_by_category(sample_transactions, categories)

    assert result["перевод"] == 1
    assert result["вклад"] == 1
    assert "оплата" not in result


def test_count_operations_by_category_no_matches() -> None:
    """Тест подсчета когда нет совпадений"""
    transactions = [{"id": 1, "description": "Другая операция", "amount": 100}]
    categories = ["перевод", "оплата"]

    result = count_operations_by_category(transactions, categories)

    assert result["перевод"] == 0
    assert result["оплата"] == 0


def test_count_operations_by_category_empty_transactions() -> None:
    """Тест подсчета с пустым списком транзакций"""
    result = count_operations_by_category([], ["перевод", "оплата"])

    assert result["перевод"] == 0
    assert result["оплата"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])