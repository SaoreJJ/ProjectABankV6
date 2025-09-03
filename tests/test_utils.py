import pytest
import json
import os
from tempfile import NamedTemporaryFile
from typing import List, Dict, Any
from src.utils import load_transactions


def test_load_valid_file() -> None:
    """Тест загрузки нормального файла"""
    test_data = [
        {"id": 1, "amount": 100, "state": "EXECUTED"},
        {"id": 2, "amount": 200, "state": "EXECUTED"}
    ]

    with NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(test_data, f)
        temp_file = f.name

    try:
        result = load_transactions(temp_file)
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[1]['amount'] == 200
    finally:
        os.remove(temp_file)


def test_load_empty_file() -> None:
    """Тест загрузки пустого файла"""
    with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name

    try:
        result = load_transactions(temp_file)
        assert result == []
    finally:
        os.remove(temp_file)


def test_load_nonexistent_file() -> None:
    """Тест загрузки несуществующего файла"""
    result = load_transactions('несуществующий_файл.json')
    assert result == []


def test_load_invalid_json() -> None:
    """Тест загрузки некорректного JSON"""
    with NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        f.write('invalid json content')
        temp_file = f.name

    try:
        result = load_transactions(temp_file)
        assert result == []
    finally:
        os.remove(temp_file)


def test_load_file_with_empty_dicts() -> None:
    """Тест загрузки файла с пустыми словарями"""
    test_data: List[Dict[str, Any]] = [{}, {"id": 1, "amount": 100}, {}]

    with NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(test_data, f)
        temp_file = f.name

    try:
        result = load_transactions(temp_file)
        assert len(result) == 1  # Только один валидный словарь
        assert result[0]['id'] == 1
    finally:
        os.remove(temp_file)