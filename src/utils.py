import json
import os
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из файла JSON

    Args:
        file_path (str): Путь к файлу JSON

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список при ошибке
    """
    try:
        # Проверяем существует ли файл
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден")
            return []

        # Проверяем не пустой ли файл
        if os.path.getsize(file_path) == 0:
            print("Файл пустой")
            return []

        # Открываем файл и читаем данные
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем что данные - это список
        if not isinstance(data, list):
            print("Данные в файле не являются списком")
            return []

        # Фильтруем пустые словари
        valid_transactions = [tx for tx in data if isinstance(tx, dict) and tx]

        print(f"Загружено {len(valid_transactions)} транзакций")
        return valid_transactions

    except json.JSONDecodeError:
        print("Ошибка декодирования JSON")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []