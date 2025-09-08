import json
import os
from typing import List, Dict, Any
import sys

# Добавляем путь к src для импорта config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import setup_logger

# Настройка логгера
utils_logger = setup_logger('utils', 'utils.log')


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из файла JSON

    Args:
        file_path (str): Путь к файлу JSON

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список при ошибке
    """
    try:
        utils_logger.info(f"Начало загрузки транзакций из файла: {file_path}")

        # Проверяем существует ли файл
        if not os.path.exists(file_path):
            error_msg = f"Файл {file_path} не найден"
            utils_logger.error(error_msg)
            print(error_msg)
            return []

        # Проверяем не пустой ли файл
        if os.path.getsize(file_path) == 0:
            error_msg = "Файл пустой"
            utils_logger.warning(error_msg)
            print(error_msg)
            return []

        # Открываем файл и читаем данные
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем что данные - это список
        if not isinstance(data, list):
            error_msg = "Данные в файле не являются списком"
            utils_logger.error(error_msg)
            print(error_msg)
            return []

        # Фильтруем пустые словари
        valid_transactions = [tx for tx in data if isinstance(tx, dict) and tx]

        utils_logger.info(f"Успешно загружено {len(valid_transactions)} транзакций")
        print(f"Загружено {len(valid_transactions)} транзакций")
        return valid_transactions

    except json.JSONDecodeError as e:
        error_msg = f"Ошибка декодирования JSON: {e}"
        utils_logger.error(error_msg)
        print(error_msg)
        return []
    except Exception as e:
        error_msg = f"Ошибка при загрузке файла: {e}"
        utils_logger.exception(error_msg)
        print(error_msg)
        return []


# Пример использования
if __name__ == "__main__":
    # Тестирование функции
    transactions = load_transactions("../data/operations.json")
    print(f"Загружено транзакций: {len(transactions)}")

