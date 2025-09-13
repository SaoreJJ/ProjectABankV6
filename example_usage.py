import sys
import os
import json

# Добавляем src в путь для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pandas_utils import FinancialDataReader, read_transactions_from_csv, read_transactions_from_excel, get_data_summary


def main():
    # Инициализация ридера
    reader = FinancialDataReader(data_dir="data")

    # Получение информации о доступных файлах
    print("Доступные файлы:")
    files = reader.list_available_files()
    for file_info in files:
        print(f"  - {file_info['filename']} ({file_info['file_size']} bytes)")

    # Чтение CSV файла
    try:
        print("\n" + "=" * 60)
        print("ЧТЕНИЕ CSV ФАЙЛА:")
        print("=" * 60)

        csv_data = read_transactions_from_csv(
            "transactions.csv",
            data_dir="data"
        )

        print(f"✓ Успешно прочитан CSV файл")
        print(f"Размер данных: {csv_data.shape}")
        print(f"Колонки: {list(csv_data.columns)}")

        if not csv_data.empty:
            print(f"\nПервые 5 строк:")
            print(csv_data.head())

            print(f"\nТипы данных:")
            print(csv_data.dtypes)

            print(f"\nПропущенные значения:")
            print(csv_data.isnull().sum())

            # Получение сводной информации
            summary = get_data_summary(csv_data)
            print(f"\nСводная информация:")
            print(f"Количество записей: {summary['shape'][0]}")
            print(f"Количество колонок: {summary['shape'][1]}")
            print(f"Память: {summary['memory_usage'] / 1024:.2f} KB")

        else:
            print("CSV файл пуст")

    except Exception as e:
        print(f"✗ Ошибка при чтении CSV: {e}")
        import traceback
        traceback.print_exc()

    # Чтение Excel файла
    try:
        print("\n" + "=" * 60)
        print("ЧТЕНИЕ EXCEL ФАЙЛА:")
        print("=" * 60)

        excel_data = read_transactions_from_excel(
            "transactions_excel.xlsx",
            data_dir="data"
        )

        print(f"✓ Успешно прочитан Excel файл")
        print(f"Размер данных: {excel_data.shape}")

        if not excel_data.empty:
            print(f"Колонки: {list(excel_data.columns)}")
            print(f"\nПервые 5 строк:")
            print(excel_data.head())

            print(f"\nТипы данных:")
            print(excel_data.dtypes)

            # Сравнение с CSV данными
            if not csv_data.empty and not excel_data.empty:
                print(f"\nСРАВНЕНИЕ CSV И EXCEL:")
                print(f"CSV размер: {csv_data.shape}")
                print(f"Excel размер: {excel_data.shape}")
                print(f"Общие колонки: {set(csv_data.columns) & set(excel_data.columns)}")

        else:
            print("Excel файл пуст")

    except Exception as e:
        print(f"✗ Ошибка при чтении Excel: {e}")
        print("Для чтения Excel файлов установите: pip install openpyxl")

    # Сохранение обработанных данных
    try:
        if not csv_data.empty:
            csv_data.to_csv("data/processed_transactions.csv", index=False, encoding='utf-8')
            print(f"\n✓ Обработанные данные сохранены в data/processed_transactions.csv")

    except Exception as e:
        print(f"✗ Ошибка при сохранении данных: {e}")


if __name__ == "__main__":
    main()