import json
import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.utils import exchange_rate, get_price_stocks_snp500, reading_xlsx

current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir / "data" / "operations.xlsx"

path_file_xlsx = os.getenv("PATH_FILE_XLSX")
path_file = os.path.dirname(os.path.abspath(__file__))

rel_file_path = os.path.join(path_file, "../logs/views.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def changing_df(path: str, date: str) -> pd.DataFrame:
    """Функция, которая возвращает датафрейм для дальнейших работ с ним."""
    df = reading_xlsx(path=path)
    date = pd.to_datetime(date, dayfirst=False)
    start_of_month = date.replace(day=1)
    df = df[
        (df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= date)
    ]
    return df


def day_time_now() -> str:
    """Функция, которая приветствует в зависимости от текущего времени суток.
    Возвращает строку приветствия в зависимости от времени."""
    hour = int(datetime.now().strftime("%H"))
    if 6 <= hour <= 12:
        return "Доброе утро"
    elif 13 <= hour <= 17:
        return "Добрый день"
    elif 18 <= hour <= 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def each_card(path: str, date: str) -> list[dict]:
    """Функция, которая возвращает список словарей с данными о картах и затратах по ним."""
    df = changing_df(path=path, date=date)
    if len(df) == 0:
        return []
    else:
        df_expanse = (
            df[
                (df["Статус"] == "OK")
                & (df["Сумма платежа"] <= 0)
                & (df["Валюта операции"] != "RUB")
                & (df["Валюта платежа"] == "RUB")
            ]
            .groupby(["Номер карты"], as_index=False)
            .agg({"Сумма платежа": "sum"})
            .rename(columns={"Сумма платежа": "Сумма операции"})
        )
        df_operation = (
            df[
                (df["Статус"] == "OK")
                & (df["Сумма операции"] <= 0)
                & (df["Валюта платежа"] != "RUB")
                & (df["Валюта операции"] == "RUB")
            ]
            .groupby(["Номер карты"], as_index=False)
            .agg({"Сумма операции": "sum"})
        )
        df_operation_2 = (
            df[
                (df["Статус"] == "OK")
                & (df["Сумма операции"] <= 0)
                & (df["Валюта платежа"] == "RUB")
                & (df["Валюта операции"] == "RUB")
            ]
            .groupby(["Номер карты"], as_index=False)
            .agg({"Сумма операции": "sum"})
        )

        df = pd.concat([df_expanse, df_operation, df_operation_2])
        df = df.groupby(["Номер карты"], as_index=False).agg({"Сумма операции": "sum"})
        df["last_digits"] = df["Номер карты"].str[1:]
        df["total_spent"] = abs(df["Сумма операции"])
        df["cashback"] = abs(round(df["total_spent"] / 100, 2))
        df = df.drop(columns={"Сумма операции", "Номер карты"})
        return df.to_dict("records")


def top_transactions(path: str, date: str) -> list[dict]:
    """Функция, которая возвращает список словарей с Топ-5 транзакций по сумме платежа."""
    df = changing_df(path=path, date=date)
    if len(df) == 0:
        return []
    else:
        df_expanse = df[
            (df["Статус"] == "OK")
            & (df["Валюта платежа"] == "RUB")
            & (df["Валюта операции"] != "RUB")
        ][["Дата операции", "Сумма платежа", "Категория", "Описание"]].rename(
            columns={"Сумма платежа": "Сумма операции"}
        )
        df_operation = df[
            (df["Статус"] == "OK")
            & (df["Валюта платежа"] != "RUB")
            & (df["Валюта операции"] == "RUB")
        ][["Дата операции", "Сумма операции", "Категория", "Описание"]]
        df_operation_2 = df[
            (df["Статус"] == "OK")
            & (df["Валюта платежа"] == "RUB")
            & (df["Валюта операции"] == "RUB")
        ][["Дата операции", "Сумма операции", "Категория", "Описание"]]

        df = pd.concat([df_expanse, df_operation, df_operation_2])
        df["Сумма операции"] = abs(df["Сумма операции"])
        df["Дата операции"] = df["Дата операции"].dt.strftime("%d.%m.%Y")
        df = df.sort_values("Сумма операции", ascending=False)[0:4]
        df = df.rename(
            columns={
                "Дата операции": "date",
                "Сумма операции": "amount",
                "Категория": "category",
                "Описание": "description",
            }
        )
        return df.to_dict("records")


def views(path: str, date: str) -> json:
    """Функция, которая возвращает json с веб-страницей."""
    return json.dumps(
        {
            "greetings": day_time_now(),
            "cards" "": each_card(path, date),
            "top_transactions": top_transactions(path, date),
            "currency_rates": exchange_rate(),
            "stock_prices": get_price_stocks_snp500(),
        },
        ensure_ascii=False,
    )


if __name__ == "__main__":
    pass
    # print(each_card(dir_transactions_excel, "02.02.2021"))
