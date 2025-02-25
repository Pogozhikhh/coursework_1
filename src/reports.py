import os
from datetime import datetime
from typing import Optional
import pandas as pd
import json

from dateutil.relativedelta import relativedelta


def decorator_with_args(file: str):
    """Функция, которая записывает результаты из spending_by_category"""

    def my_big_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                absolute_file_path = os.path.abspath(file)
                # Убедимся, что папка для файла существует
                os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
                with open(file, "w", encoding="utf-8") as file_2:
                    json.dump(result.to_dict("records"), file_2, ensure_ascii=False)
                return result
            except FileNotFoundError:
                print("Не получилось записать информацию в файл")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        return wrapper

    return my_big_decorator


@decorator_with_args(
    "C:/Users/111/PycharmProjects/coursework_1/logs/decorators_mistakes.json"
)
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = str(datetime.now())
) -> pd.DataFrame:
    """Функция, которая возвращает датафрейм с тратами по заданной категории
    за последние три месяца (от переданной даты)."""
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], dayfirst=True
    )
    transactions_by_category = transactions[
        (
            transactions["Дата операции"]
            <= (pd.to_datetime(date, dayfirst=True) + relativedelta(months=2))
        )
        & (transactions["Дата операции"] >= pd.to_datetime(date, dayfirst=True))
        & (transactions["Категория"].str.upper() == category.upper())
    ]
    trans = pd.DataFrame(
        transactions_by_category.groupby(["Категория"], as_index=False)
        .agg({"Сумма операции": "sum"})["Сумма операции"]
        .rename({"Сумма операции": category})
    )
    return trans


if __name__ == "__main__":
    # Создаем пример DataFrame с транзакциями
    data = {
        "Дата операции": ["01/01/2023", "15/01/2023", "20/02/2023", "10/03/2023"],
        "Категория": ["Food", "Transport", "Food", "Utilities"],
        "Сумма операции": [100, 50, 75, 200],
    }
    transactions_df = pd.DataFrame(data)

    # Вызываем функцию
    result = spending_by_category(transactions_df, category="Food", date="01/01/2023")
    print(result)
