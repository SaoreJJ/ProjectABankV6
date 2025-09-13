import pytest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch, mock_open
import io

# Импортируем тестируемый класс
from src.pandas_utils import FinancialDataReader, read_transactions_from_csv, read_transactions_from_excel, get_data_summary


class TestFinancialDataReader:
    """Тесты для класса FinancialDataReader"""

    @pytest.fixture
    def setup_test_data(self):
        """Создание временной директории с тестовыми файлами"""
        self.test_dir = tempfile.mkdtemp()

        # Создаем тестовый CSV файл
        self.csv_data = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'Amount': [100.50, -50.25, 75.00],
            'Description': ['Salary', 'Groceries', 'Bonus'],
            'Category': ['Income', 'Food', 'Income']
        })
        self.csv_path = os.path.join(self.test_dir, 'test_transactions.csv')
        self.csv_data.to_csv(self.csv_path, index=False)

        # Создаем тестовый Excel файл
        self.excel_path = os.path.join(self.test_dir, 'test_transactions.xlsx')
        self.csv_data.to_excel(self.excel_path, index=False)

        # Создаем файл с проблемными данными
        self.problem_csv_path = os.path.join(self.test_dir, 'problem_data.csv')
        problem_data = pd.DataFrame({
            'Date with spaces': ['2023-01-01', 'invalid_date'],
            'Amount $': ['100.50', 'not_a_number'],
            '  Extra Spaces  ': ['value1', 'value2'],
            'Unnamed: 3': [None, None]
        })
        problem_data.to_csv(self.problem_csv_path, index=False)

        yield

        # Очистка после тестов
        shutil.rmtree(self.test_dir)

    def test_init_with_custom_directory(self):
        """Тест инициализации с пользовательской директорией"""
        reader = FinancialDataReader('/custom/path')
        assert reader.data_dir == '/custom/path'

    def test_init_with_default_directory(self):
        """Тест инициализации с директорией по умолчанию"""
        reader = FinancialDataReader()
        assert reader.data_dir == "../data"

    def test_read_csv_transactions_success(self, setup_test_data):
        """Тест успешного чтения CSV файла"""
        reader = FinancialDataReader(self.test_dir)

        # Тест возврата DataFrame
        result_df = reader.read_csv_transactions('test_transactions.csv', return_type='dataframe')
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 3
        assert list(result_df.columns) == ['date', 'amount', 'description', 'category']

        # Тест возврата списка словарей
        result_list = reader.read_csv_transactions('test_transactions.csv', return_type='list_of_dicts')
        assert isinstance(result_list, list)
        assert len(result_list) == 3
        assert all(isinstance(item, dict) for item in result_list)

    def test_read_csv_transactions_file_not_found(self):
        """Тест обработки отсутствующего файла"""
        reader = FinancialDataReader('/non/existent/path')

        with pytest.raises(FileNotFoundError):
            reader.read_csv_transactions('nonexistent.csv')

    def test_read_excel_transactions_success(self, setup_test_data):
        """Тест успешного чтения Excel файла"""
        reader = FinancialDataReader(self.test_dir)

        # Тест возврата DataFrame
        result_df = reader.read_excel_transactions('test_transactions.xlsx', return_type='dataframe')
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 3

        # Тест возврата списка словарей
        result_list = reader.read_excel_transactions('test_transactions.xlsx', return_type='list_of_dicts')
        assert isinstance(result_list, list)
        assert len(result_list) == 3

    def test_read_excel_transactions_file_not_found(self):
        """Тест обработки отсутствующего Excel файла"""
        reader = FinancialDataReader('/non/existent/path')

        with pytest.raises(FileNotFoundError):
            reader.read_excel_transactions('nonexistent.xlsx')

    def test_clean_column_names(self):
        """Тест очистки названий колонок"""
        reader = FinancialDataReader()

        test_columns = pd.Index(['Date Column', 'Amount ($)', '  Description  ', None, ''])
        cleaned = reader._clean_column_names(test_columns)

        # Правильный ожидаемый результат на основе реального поведения кода
        expected = ['date_column', 'amount', 'description', 'column_3', 'column_4']
        assert cleaned == expected

    def test_infer_data_types(self):
        """Тест автоматического определения типов данных"""
        reader = FinancialDataReader()

        test_df = pd.DataFrame({
            'date_col': ['2023-01-01', '2023-01-02'],
            'numeric_col': ['100.50', '200.75'],
            'string_col': ['  text  ', 'more text  '],
            'mixed_col': ['text', '123']
        })

        result = reader._infer_data_types(test_df)

        # Проверяем преобразование даты
        assert pd.api.types.is_datetime64_any_dtype(result['date_col'])

        # Проверяем преобразование чисел
        assert pd.api.types.is_numeric_dtype(result['numeric_col'])

        # Проверяем очистку строк
        assert result['string_col'].iloc[0] == 'text'

    def test_process_dataframe(self):
        """Тест обработки DataFrame"""
        reader = FinancialDataReader()

        # Создаем DataFrame с проблемами
        test_df = pd.DataFrame({
            '  Date  ': ['2023-01-01', None],
            'Amount': ['100.50', '200.75'],
            'Unnamed: 2': [None, None]
        })

        result = reader._process_dataframe(test_df)

        # Проверяем очистку колонок
        assert 'date' in result.columns
        assert 'unnamed_2' not in result.columns

        # Проверяем удаление пустых строк
        assert len(result) == 2

    def test_get_data_summary(self):
        """Тест получения сводной информации"""
        reader = FinancialDataReader()

        test_df = pd.DataFrame({
            'date': pd.to_datetime(['2023-01-01', '2023-01-02']),
            'amount': [100.50, 200.75],
            'category': ['A', 'B']
        })

        summary = reader.get_data_summary(test_df)

        assert summary['shape'] == (2, 3)
        assert 'date' in summary['columns']
        assert 'numeric_stats' in summary

    def test_get_data_summary_empty(self):
        """Тест сводной информации для пустого DataFrame"""
        reader = FinancialDataReader()

        empty_df = pd.DataFrame()
        summary = reader.get_data_summary(empty_df)

        assert summary['message'] == "DataFrame пуст"

    def test_get_file_info(self, setup_test_data):
        """Тест получения информации о файле"""
        reader = FinancialDataReader(self.test_dir)

        info = reader.get_file_info('test_transactions.csv')

        assert info['filename'] == 'test_transactions.csv'
        assert info['file_extension'] == '.csv'
        assert info['file_size'] > 0

    def test_get_file_info_not_found(self):
        """Тест информации о несуществующем файле"""
        reader = FinancialDataReader('/non/existent/path')

        info = reader.get_file_info('nonexistent.csv')
        assert 'error' in info

    def test_list_available_files(self, setup_test_data):
        """Тест списка доступных файлов"""
        reader = FinancialDataReader(self.test_dir)

        files = reader.list_available_files()

        filenames = [f['filename'] for f in files]
        assert 'test_transactions.csv' in filenames
        assert 'test_transactions.xlsx' in filenames

    def test_list_available_files_empty_dir(self):
        """Тест списка файлов в пустой директории"""
        empty_dir = tempfile.mkdtemp()
        reader = FinancialDataReader(empty_dir)

        files = reader.list_available_files()
        assert files == []

        shutil.rmtree(empty_dir)


class TestConvenienceFunctions:
    """Тесты для удобных функций"""

    @pytest.fixture
    def setup_test_files(self):
        """Создание тестовых файлов"""
        self.test_dir = tempfile.mkdtemp()

        # CSV файл
        self.csv_path = os.path.join(self.test_dir, 'test.csv')
        test_data = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02'],
            'Amount': [100, 200],
            'Description': ['Test1', 'Test2']
        })
        test_data.to_csv(self.csv_path, index=False)

        # Excel файл
        self.excel_path = os.path.join(self.test_dir, 'test.xlsx')
        test_data.to_excel(self.excel_path, index=False)

        yield

        shutil.rmtree(self.test_dir)

    def test_read_transactions_from_csv(self, setup_test_files):
        """Тест функции read_transactions_from_csv"""
        result = read_transactions_from_csv(self.csv_path)

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, dict) for item in result)
        assert 'date' in result[0]

    def test_read_transactions_from_excel(self, setup_test_files):
        """Тест функции read_transactions_from_excel"""
        result = read_transactions_from_excel(self.excel_path)

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, dict) for item in result)

    def test_get_data_summary_function(self):
        """Тест функции get_data_summary"""
        test_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })

        summary = get_data_summary(test_df)

        assert summary['shape'] == (3, 2)
        assert 'col1' in summary['columns']


class TestErrorHandling:
    """Тесты обработки ошибок"""

    def test_csv_read_error_handling(self):
        """Тест обработки ошибок при чтении CSV"""
        reader = FinancialDataReader('/invalid/path')

        with pytest.raises(FileNotFoundError):
            reader.read_csv_transactions('nonexistent.csv')

    def test_excel_read_error_handling(self):
        """Тест обработки ошибок при чтении Excel"""
        reader = FinancialDataReader('/invalid/path')

        with pytest.raises(FileNotFoundError):
            reader.read_excel_transactions('nonexistent.xlsx')

    def test_missing_libraries_handling(self):
        """Тест обработки отсутствующих библиотек"""
        reader = FinancialDataReader()

        with patch('pandas.read_excel') as mock_read:
            mock_read.side_effect = ImportError("No module named 'openpyxl'")

            with pytest.raises(ImportError):
                # Создаем временный файл для теста
                with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                    tmp_path = tmp.name

                try:
                    reader.read_excel_transactions(tmp_path)
                finally:
                    os.unlink(tmp_path)


class TestEdgeCases:
    """Тесты крайних случаев"""

    def test_empty_dataframe_processing(self):
        """Тест обработки пустого DataFrame"""
        reader = FinancialDataReader()

        empty_df = pd.DataFrame()
        result = reader._process_dataframe(empty_df)

        assert result.empty

    def test_all_null_columns(self):
        """Тест DataFrame со всеми пустыми колонками"""
        reader = FinancialDataReader()

        test_df = pd.DataFrame({
            'col1': [None, None],
            'col2': [None, None]
        })

        result = reader._process_dataframe(test_df)
        # Пустые колонки должны быть удалены
        assert len(result.columns) == 0

    def test_duplicate_column_names(self):
        """Тест обработки дублирующихся названий колонок"""
        reader = FinancialDataReader()

        test_df = pd.DataFrame({
            'col': [1, 2],
            'col_1': [3, 4]  # pandas автоматически переименовывает дубликаты
        })
        test_df.columns = ['col', 'col']  # Принудительно создаем дубликаты

        result = reader._process_dataframe(test_df)
        # Должны быть уникальные имена колонок
        assert len(set(result.columns)) == len(result.columns)


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v"])