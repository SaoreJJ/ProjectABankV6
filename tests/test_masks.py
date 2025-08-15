import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestAccountMasking:
    """Тесты для функции маскировки номеров счетов"""

    def test_standard_account_mask(self):
        """Тест стандартной маскировки счета"""
        assert get_mask_account("12345678901234567890") == "**7890"


# Параметризованные тесты для проверки нескольких случаев
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("1111222233334444", "1111 22** **** 4444"),
        (9999888877776666, "9999 88** **** 6666"),
    ],
)
def test_parametrized_card_masking(card_number, expected):
    """Параметризованный тест для разных номеров карт"""
    assert get_mask_card_number(card_number) == expected
