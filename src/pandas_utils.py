import pandas as pd
import os
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import logging
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialDataReader:
    """Класс для чтения финансовых операций из различных форматов файлов"""

    def __init__(self, data_dir: str = "../data"):
        """
        Инициализация ридера финансовых данных

        Args:
            data_dir: Путь к директории с данными
        """
        self.data_dir = data_dir
        self.supported_formats = [".csv", ".xlsx", ".xls"]

    def read_csv_transactions(
        self, filename: str = "transactions.csv", return_type: str = "list_of_dicts", **kwargs
    ) -> Union[pd.DataFrame, List[Dict]]:
        """
        Чтение финансовых операций из CSV файла

        Args:
            filename: Имя CSV файла
            return_type: Тип возвращаемых данных ('dataframe' или 'list_of_dicts')
            **kwargs: Дополнительные параметры для pd.read_csv()

        Returns:
            DataFrame или список словарей с финансовыми операциями
        """
        try:
            file_path = os.path.join(self.data_dir, filename)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {filename} не найден в {self.data_dir}")

            # Параметры по умолчанию для CSV
            default_kwargs = {"encoding": "utf-8", "sep": ",", "engine": "python", "on_bad_lines": "skip"}
            default_kwargs.update(kwargs)

            df = pd.read_csv(file_path, **default_kwargs)

            logger.info(f"Успешно прочитан CSV файл: {filename}")
            logger.info(f"Размер данных: {df.shape}")
            logger.info(f"Колонки: {list(df.columns)}")

            processed_df = self._process_dataframe(df)

            if return_type.lower() == "list_of_dicts":
                return processed_df.to_dict("records")
            else:
                return processed_df

        except Exception as e:
            logger.error(f"Ошибка при чтении CSV файла {filename}: {str(e)}")
            raise

    def read_excel_transactions(
        self,
        filename: str = "transactions_excel.xlsx",
        sheet_name: Union[str, int, None] = 0,
        return_type: str = "list_of_dicts",
        **kwargs,
    ) -> Union[pd.DataFrame, List[Dict]]:
        """
        Чтение финансовых операций из Excel файла

        Args:
            filename: Имя Excel файла
            sheet_name: Имя листа или индекс (0 для первого листа)
            return_type: Тип возвращаемых данных ('dataframe' или 'list_of_dicts')
            **kwargs: Дополнительные параметры для pd.read_excel()

        Returns:
            DataFrame или список словарей с финансовыми операциями
        """
        try:
            file_path = os.path.join(self.data_dir, filename)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл {filename} не найден в {self.data_dir}")

            # Определяем движок в зависимости от расширения файла
            file_ext = os.path.splitext(filename)[1].lower()

            if file_ext == ".xlsx":
                engine = "openpyxl"
            elif file_ext == ".xls":
                engine = "xlrd"
            else:
                engine = None

            # Параметры по умолчанию для Excel
            default_kwargs = {"sheet_name": sheet_name, "engine": engine}
            default_kwargs.update(kwargs)

            df = pd.read_excel(file_path, **default_kwargs)

            logger.info(f"Успешно прочитан Excel файл: {filename}")
            logger.info(f"Размер данных: {df.shape}")
            if not df.empty:
                logger.info(f"Колонки: {list(df.columns)}")

            processed_df = self._process_dataframe(df)

            if return_type.lower() == "list_of_dicts":
                return processed_df.to_dict("records")
            else:
                return processed_df

        except ImportError as e:
            logger.error(f"Не установлена необходимая библиотека: {str(e)}")
            logger.error("Установите: pip install openpyxl xlrd")
            raise
        except Exception as e:
            logger.error(f"Ошибка при чтении Excel файла {filename}: {str(e)}")
            raise

    def _process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Обработка DataFrame: очистка и стандартизация данных

        Args:
            df: Исходный DataFrame

        Returns:
            Обработанный DataFrame
        """
        if df.empty:
            return df

        # Создаем копию для избежания изменения оригинальных данных
        processed_df = df.copy()

        # Очистка названий колонок
        processed_df.columns = self._clean_column_names(processed_df.columns)

        # Автоматическое определение типов данных
        processed_df = self._infer_data_types(processed_df)

        # Удаление полностью пустых строк
        processed_df = processed_df.dropna(how="all")

        # Удаление полностью пустых колонок
        processed_df = processed_df.dropna(axis=1, how="all")

        # Сброс индекса
        processed_df = processed_df.reset_index(drop=True)

        return processed_df

    def _clean_column_names(self, columns: pd.Index) -> List[str]:
        """
        Очистка названий колонок

        Args:
            columns: Исходные названия колонок

        Returns:
            Очищенные названия колонок
        """
        cleaned_columns = []
        for col in columns:
            if pd.isna(col):
                cleaned = f"column_{len(cleaned_columns)}"
            else:
                # Приведение к нижнему регистру, удаление пробелов и специальных символов
                cleaned = str(col).strip().lower()
                cleaned = re.sub(r"[^\w]", "_", cleaned)  # Замена не-буквенных символов на _
                cleaned = re.sub(r"_+", "_", cleaned)  # Удаление повторяющихся _
                cleaned = cleaned.strip("_")

                if not cleaned:  # Если после очистки строка пустая
                    cleaned = f"column_{len(cleaned_columns)}"

            # Убедимся, что имя колонки уникально
            base_name = cleaned
            counter = 1
            while cleaned in cleaned_columns:
                cleaned = f"{base_name}_{counter}"
                counter += 1

            cleaned_columns.append(cleaned)

        return cleaned_columns

    def _infer_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Автоматическое определение типов данных

        Args:
            df: DataFrame для обработки

        Returns:
            DataFrame с преобразованными типами данных
        """
        processed_df = df.copy()

        for col in processed_df.columns:
            # Пропускаем пустые колонки
            if processed_df[col].isna().all():
                continue

            # Попытка преобразовать в числовой тип
            try:
                numeric_col = pd.to_numeric(processed_df[col], errors="coerce")
                if not numeric_col.isna().all():  # Если есть хотя бы одно число
                    processed_df[col] = numeric_col
                    continue
            except:
                pass

            # Попытка преобразовать в дату (только для колонок с названием содержащим 'date')
            if "date" in col.lower():
                try:
                    # Пробуем разные форматы дат
                    date_formats = [
                        "%Y-%m-%d %H:%M:%S",
                        "%Y-%m-%d",
                        "%d.%m.%Y %H:%M:%S",
                        "%d.%m.%Y",
                        "%m/%d/%Y",
                        "%d/%m/%Y",
                    ]

                    for date_format in date_formats:
                        try:
                            date_col = pd.to_datetime(processed_df[col], format=date_format, errors="coerce")
                            if not date_col.isna().all():
                                processed_df[col] = date_col
                                break
                        except:
                            continue
                    else:
                        # Если ни один формат не подошел, пробуем без указания формата
                        date_col = pd.to_datetime(processed_df[col], errors="coerce")
                        if not date_col.isna().all():
                            processed_df[col] = date_col

                except Exception as e:
                    logger.warning(f"Не удалось преобразовать колонку {col} в дату: {str(e)}")

            # Для строковых данных убираем лишние пробелы
            if processed_df[col].dtype == "object":
                processed_df[col] = processed_df[col].astype(str).str.strip()

        return processed_df

    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Получение сводной информации о данных

        Args:
            df: DataFrame для анализа

        Returns:
            Словарь с информацией о данных
        """
        if df.empty:
            return {"message": "DataFrame пуст"}

        summary = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "missing_values": df.isnull().sum().to_dict(),
            "unique_counts": {col: df[col].nunique() for col in df.columns},
            "memory_usage": df.memory_usage(deep=True).sum(),
        }

        # Добавляем информацию о числовых колонках
        numeric_cols = df.select_dtypes(include=["number"]).columns
        if not numeric_cols.empty:
            summary["numeric_stats"] = df[numeric_cols].describe().to_dict()

        return summary

    def get_file_info(self, filename: str) -> Dict[str, Any]:
        """
        Получение информации о файле

        Args:
            filename: Имя файла

        Returns:
            Словарь с информацией о файле
        """
        file_path = os.path.join(self.data_dir, filename)

        if not os.path.exists(file_path):
            return {"error": "Файл не найден"}

        file_info = {
            "filename": filename,
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "file_extension": os.path.splitext(filename)[1],
            "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)),
        }

        return file_info

    def list_available_files(self) -> List[Dict[str, Any]]:
        """
        Список доступных файлов в директории данных

        Returns:
            Список информации о файлах
        """
        files_info = []

        if os.path.exists(self.data_dir):
            for file in os.listdir(self.data_dir):
                if any(file.endswith(ext) for ext in self.supported_formats):
                    files_info.append(self.get_file_info(file))

        return files_info


# Функции для удобного использования
def read_transactions_from_csv(file_path: str, **kwargs) -> List[Dict]:
    """
    Функция для считывания финансовых операций из CSV.
    Принимает путь к файлу CSV в качестве аргумента.
    Выдает список словарей с транзакциями.

    Args:
        file_path: Полный путь к CSV файлу
        **kwargs: Дополнительные параметры для pd.read_csv()

    Returns:
        Список словарей с финансовыми операциями
    """
    # Извлекаем директорию и имя файла из полного пути
    data_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    reader = FinancialDataReader(data_dir)
    kwargs.pop("return_type", None)  # Убедимся, что возвращается список словарей
    return reader.read_csv_transactions(filename, return_type="list_of_dicts", **kwargs)


def read_transactions_from_excel(file_path: str, **kwargs) -> List[Dict]:
    """
    Функция для считывания финансовых операций из Excel.
    Принимает путь к файлу Excel в качестве аргумента.
    Выдает список словарей с транзакциями.

    Args:
        file_path: Полный путь к Excel файлу
        **kwargs: Дополнительные параметры для pd.read_excel()

    Returns:
        Список словарей с финансовыми операциями
    """
    # Извлекаем директорию и имя файла из полного пути
    data_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    reader = FinancialDataReader(data_dir)
    kwargs.pop("return_type", None)  # Убедимся, что возвращается список словарей
    return reader.read_excel_transactions(filename, return_type="list_of_dicts", **kwargs)


def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Удобная функция для получения сводной информации о данных

    Args:
        df: DataFrame для анализа

    Returns:
        Словарь с информацией о данных
    """
    reader = FinancialDataReader()
    return reader.get_data_summary(df)
