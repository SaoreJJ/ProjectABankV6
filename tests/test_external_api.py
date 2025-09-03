import pytest
import requests
from unittest.mock import patch, MagicMock
from typing import Dict, Any
from src.external_api import get_amount_in_rubles, get_exchange_rate


def test_get_amount_in_rubles_rub() -> None:
    """Тест для рублевых транзакций"""
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "100.50", "currency": {"code": "RUB", "name": "руб."}}
    }

    result = get_amount_in_rubles(transaction)
    assert result == 100.50


def test_get_amount_in_rubles_usd() -> None:
    """Тест для долларовых транзакций с mock API"""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "USD"}}}

    with patch("src.external_api.get_exchange_rate") as mock_rate:
        mock_rate.return_value = 75.0
        result = get_amount_in_rubles(transaction)
        assert result == 7500.0
        mock_rate.assert_called_once_with("USD", "RUB")


def test_get_amount_in_rubles_eur() -> None:
    """Тест для евро транзакций с mock API"""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR", "name": "EUR"}}}

    with patch("src.external_api.get_exchange_rate") as mock_rate:
        mock_rate.return_value = 85.0
        result = get_amount_in_rubles(transaction)
        assert result == 4250.0
        mock_rate.assert_called_once_with("EUR", "RUB")


def test_get_amount_in_rubles_invalid_transaction() -> None:
    """Тест для некорректной транзакции"""
    transaction: Dict[str, Any] = {"id": 1}
    result = get_amount_in_rubles(transaction)
    assert result == 0.0


def test_get_amount_in_rubles_missing_currency() -> None:
    """Тест для транзакции с отсутствующей валютой"""
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "100.00"}
    }
    result = get_amount_in_rubles(transaction)
    assert result == 0.0


def test_get_amount_in_rubles_invalid_amount() -> None:
    """Тест для некорректной суммы"""
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "invalid", "currency": {"code": "RUB", "name": "руб."}}
    }
    result = get_amount_in_rubles(transaction)
    assert result == 0.0


def test_get_amount_in_rubles_unknown_currency() -> None:
    """Тест для неизвестной валюты"""
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "100.00", "currency": {"code": "GBP", "name": "GBP"}}
    }

    with patch("src.external_api.get_exchange_rate") as mock_rate:
        result = get_amount_in_rubles(transaction)
        assert result == 100.0
        mock_rate.assert_not_called()


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_get_exchange_rate_success(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест успешного получения курса валют"""
    mock_getenv.return_value = "test_api_token"

    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 75.5}, "success": True}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_exchange_rate("USD", "RUB")
    assert result == 75.5
    mock_get.assert_called_once()
    mock_getenv.assert_called_with("API_LAYER_TOKEN")


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_get_exchange_rate_failure(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест неудачного получения курса валют"""
    mock_getenv.return_value = "test_api_token"
    mock_get.side_effect = requests.exceptions.RequestException("API error")

    result = get_exchange_rate("USD", "RUB")
    assert result == 1.0


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_get_exchange_rate_connection_error(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест ошибки соединения"""
    mock_getenv.return_value = "test_api_token"
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

    result = get_exchange_rate("USD", "RUB")
    assert result == 1.0


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_get_exchange_rate_timeout(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест таймаута"""
    mock_getenv.return_value = "test_api_token"
    mock_get.side_effect = requests.exceptions.Timeout("Timeout error")

    result = get_exchange_rate("USD", "RUB")
    assert result == 1.0


@patch("src.external_api.os.getenv")
def test_get_exchange_rate_no_token(mock_getenv: MagicMock) -> None:
    """Тест получения курса без API токена"""
    mock_getenv.return_value = None

    result = get_exchange_rate("USD", "RUB")
    assert result == 1.0


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_get_exchange_rate_invalid_response(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест некорректного ответа API"""
    mock_getenv.return_value = "test_api_token"

    mock_response = MagicMock()
    mock_response.json.return_value = {"error": "Invalid request", "success": False}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_exchange_rate("USD", "RUB")
    assert result == 1.0


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_get_exchange_rate_missing_rates(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест ответа без rates"""
    mock_getenv.return_value = "test_api_token"

    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}  # Нет rates
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_exchange_rate("USD", "RUB")
    assert result == 1.0


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_get_exchange_rate_default_parameters(mock_getenv: MagicMock, mock_get: MagicMock) -> None:
    """Тест вызова с параметрами по умолчанию"""
    mock_getenv.return_value = "test_token"
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 75.0}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_exchange_rate("USD")
    assert result == 75.0