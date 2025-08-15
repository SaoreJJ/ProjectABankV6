from datetime import datetime

import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции mask_account_card"""

    @pytest.mark.parametrize(
        "input_str, expected",
        [
            # Тесты для карт
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
            ("МИР 1234123412341234", "МИР 1234 12** **** 1234"),
            ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
        ],
    )
    def test_mask_account_card_valid(self, input_str: str, expected: str) -> None:
        """Тест маскировки валидных номеров карт и счетов"""
        assert mask_account_card(input_str) == expected


class TestGetDate:
    @pytest.mark.parametrize(
        "invalid_date",
        [
            "",
            "2023/01/01 12:00:00",
            "01-01-2023",
            "not-a-date",
            1234567890,  # число вместо строки
            None,  # None значение
        ],
    )
    def test_get_date_invalid(self, invalid_date: str) -> None:
        """Тест невалидных форматов даты"""
        with pytest.raises((ValueError, AttributeError, TypeError)):
            get_date(invalid_date)


def test_edge_case_special_characters() -> None:
    """Тест специальных символов в названии карты"""
    assert mask_account_card("Special!@# 1234567890123456") == "Special!@# 1234 56** **** 3456"
