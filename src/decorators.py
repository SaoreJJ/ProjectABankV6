import datetime


def log(filename=None):
    """
    Простой декоратор для логирования функций
    filename: если указан - пишет в файл, если нет - в консоль
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Пытаемся выполнить функцию
            try:
                # Вызываем оригинальную функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                message = f"{func.__name__} ok\n"

            except Exception as e:
                # Если произошла ошибка
                result = None
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                # Пробрасываем ошибку дальше
                raise

            finally:
                # Записываем лог в файл или консоль
                if filename:
                    # Добавляем время для файла
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    full_message = f"{timestamp} - {message}"
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(full_message)
                else:
                    # Просто выводим в консоль
                    print(message, end="")

            return result

        return wrapper

    return decorator
