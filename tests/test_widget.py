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
