import sys
import unittest
from pathlib import Path
from typing import Any, Dict, List

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card

# Добавление пути для импортов
sys.path.append(str(Path(__file__).parent))


class TestBankFunctions(unittest.TestCase):
    """Основные тесты для всех функций банковского проекта."""

    def setUp(self) -> None:
        """Инициализация тестовых данных."""
        self.test_transactions: List[Dict[str, Any]] = [
            {"id": 1, "state": "EXECUTED", "date": "2023-01-15T10:30:00.000000"},
            {"id": 2, "state": "CANCELED", "date": "2023-01-10T12:00:00.000000"},
            {"id": 3, "state": "EXECUTED", "date": "2023-01-20T08:45:00.000000"},
            {"id": 4, "state": "PENDING", "date": "2023-01-05T14:15:00.000000"},
        ]

    def test_card_masking(self) -> None:
        """Тест маскировки номеров карт."""
        self.assertEqual(get_mask_card_number("7000792289606361"), "7000 79** **** 6361")
        self.assertEqual(get_mask_card_number("1234567812345678"), "1234 56** **** 5678")

    def test_account_masking(self) -> None:
        """Тест маскировки номеров счетов."""
        self.assertEqual(get_mask_account("73654108430135874305"), "**4305")
        self.assertEqual(get_mask_account("12345678901234567890"), "**7890")

    def test_account_card_formatting(self) -> None:
        """Тест форматирования карт/счетов."""
        self.assertEqual(
            mask_account_card("Visa Platinum 7000792289606361"),
            "Visa Platinum 7000 79** **** 6361"
        )

    def test_date_formatting(self) -> None:
        """Тест форматирования дат."""
        self.assertEqual(get_date("2018-07-11T02:26:18.671407"), "11.07.2018")
        self.assertEqual(get_date("2022-12-31T23:59:59.999999"), "31.12.2022")

    def test_state_filtering(self) -> None:
        """Тест фильтрации по состоянию."""
        executed = filter_by_state(self.test_transactions)
        self.assertEqual(len(executed), 2)
        self.assertEqual(executed[0]["id"], 1)

        canceled = filter_by_state(self.test_transactions, "CANCELED")
        self.assertEqual(len(canceled), 1)

    def test_date_sorting(self) -> None:
        """Тест сортировки по дате."""
        sorted_desc = sort_by_date(self.test_transactions)
        self.assertEqual(sorted_desc[0]["id"], 3)
        self.assertEqual(sorted_desc[-1]["id"], 4)


class TestErrorHandling(unittest.TestCase):
    """Тесты обработки ошибок и граничных случаев."""

    def test_invalid_card_numbers(self) -> None:
        """Тест невалидных номеров карт."""
        with self.assertRaises(ValueError):
            get_mask_card_number("123")
        with self.assertRaises(ValueError):
            get_mask_card_number("abcdefghijklmnop")

    def test_invalid_account_numbers(self) -> None:
        """Тест невалидных номеров счетов."""
        with self.assertRaises(ValueError):
            get_mask_account("123")
        with self.assertRaises(ValueError):
            get_mask_account("abcde")

    def test_empty_data_handling(self) -> None:
        """Тест обработки пустых данных."""
        self.assertEqual(filter_by_state([]), [])


if __name__ == "__main__":
    unittest.main()
