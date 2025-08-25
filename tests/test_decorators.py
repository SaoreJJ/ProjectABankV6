import os
from typing import Any
import pytest
from src.decorators import log


def test_log_to_console_success(capsys: Any) -> None:
    """Тест: логирование успеха в консоль"""

    @log()
    def test_add(a: int, b: int) -> int:
        return a + b

    # Вызываем функцию
    result: int = test_add(2, 3)

    # Проверяем результат
    assert result == 5

    # Проверяем что вывелось в консоль
    captured = capsys.readouterr()
    assert "test_add ok" in captured.out


def test_log_to_file_error() -> None:
    """Тест: логирование ошибки в файл"""
    filename: str = "test_error.log"

    if os.path.exists(filename):
        os.remove(filename)

    @log(filename=filename)
    def test_divide(a: int, b: int) -> float:
        if b == 0:
            raise ZeroDivisionError("Деление на ноль")
        return a / b

    # Вызываем функцию которая упадет
    try:
        test_divide(10, 0)
    except ZeroDivisionError:
        pass  # Ожидаем ошибку

    # Проверяем что записалось в файл
    assert os.path.exists(filename)

    with open(filename, "r", encoding="utf-8") as f:
        content: str = f.read()
        assert "test_divide error: ZeroDivisionError" in content
        assert "Inputs: (10, 0), {}" in content

    # Убираем за собой
    os.remove(filename)


def test_log_with_arguments(capsys: Any) -> None:
    """Тест: логирование с аргументами"""

    @log()
    def test_greet(name: str, age: int = 25) -> str:
        return f"Привет {name}, тебе {age} лет"

    # Вызываем с разными аргументами
    result: str = test_greet("Анна", age=30)
    assert "Анна" in result

    # Проверяем лог
    captured = capsys.readouterr()
    assert "test_greet ok" in captured.out


def test_error_propagation() -> None:
    """Тест: что ошибки не проглатываются"""
    @log()
    def test_crash() -> None:
        raise RuntimeError("Важная ошибка")

    # Убеждаемся что ошибка пробрасывается
    with pytest.raises(RuntimeError):
        test_crash()




