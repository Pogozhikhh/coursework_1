import json
import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir / "data" / "operations.xlsx"
user_setting = current_dir / "user_settings.json"

path_file = os.path.dirname(os.path.abspath(__file__))

rel_file_path = os.path.join(path_file, "../logs/utils.log")
abs_file_path = os.path.abspath(rel_file_path)


logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def reading_json_file(path: str) -> list[dict]:
    """Функция, которая принимает на вход путь до JSON-файла
    и возвращает список словарей с пользовательскими параметрами"""
    try:
        logger.info("Попытка открыть JSON-файл")
        with open(path, encoding="utf-8") as f:
            lst = json.load(f)
        if not isinstance(lst, list) or not lst:
            logger.warning("Проблема с содержимым JSON-файла")
            return []
        else:
            return lst
    except FileNotFoundError:
        logger.warning("Возможна проблема с путем до JSON-файла")
        return []


def reading_xlsx(path: str) -> pd.DataFrame:
    """Функция, которая принимает на вход путь до XLSX-файла
    и возвращает датафрейм по операциям."""
    try:
        fieldnames = {
            "Дата операции": str,
            "Номер карты": str,
            "Статус": str,
            "Сумма операции": float,
            "Валюта операции": str,
            "Сумма платежа": float,
            "Валюта платежа": str,
            "Категория": str,
            "Описание": str,
        }
        df = pd.read_excel(path, decimal=";", dtype=fieldnames)[
            [
                "Дата операции",
                "Номер карты",
                "Статус",
                "Сумма операции",
                "Валюта операции",
                "Сумма платежа",
                "Валюта платежа",
                "Категория",
                "Описание",
            ]
        ]
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        return df
    except FileNotFoundError:
        return pd.DataFrame()


def df_to_transactions(lst: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Функция, которая возвращает список для дальнейших работ с ним."""
    df = pd.DataFrame(lst)
    df_expanse = (
        df[
            (df["Статус"] == "OK")
            & (df["Сумма платежа"] <= 0)
            & (df["Валюта операции"] != "RUB")
            & (df["Валюта платежа"] == "RUB")
        ]
        .groupby(["Дата операции"], as_index=False)
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
        .groupby(["Дата операции"], as_index=False)
        .agg({"Сумма операции": "sum"})
    )
    df_operation_2 = (
        df[
            (df["Статус"] == "OK")
            & (df["Сумма операции"] <= 0)
            & (df["Валюта платежа"] == "RUB")
            & (df["Валюта операции"] == "RUB")
        ]
        .groupby(["Дата операции"], as_index=False)
        .agg({"Сумма операции": "sum"})
    )

    df = pd.concat([df_expanse, df_operation, df_operation_2])
    df = df.groupby(["Дата операции"], as_index=False).agg({"Сумма операции": "sum"})
    transactions = df.to_dict("records")
    return transactions


def exchange_rate() -> list:
    """Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API."""
    load_dotenv()
    apikey = os.getenv("API-KEY_EXCHANGE")
    headers = {"apikey": f"{apikey}"}
    user_currencies = reading_json_file(
        user_setting
    )[0]["user_currencies"]
    lst = []
    try:
        for i in user_currencies:
            logger.info("Попытка подключения через API к сайту с курсом валют")
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={i}&amount=1"
            response = requests.get(url, headers=headers)
            dct = {"currency": i, "rate": round(response.json()["info"]["rate"], 2)}
            logger.info("Успешное подключение через API к сайту с курсом валют")
            lst.append(dct)
        return lst
    except requests.exceptions.RequestException:
        logger.warning(
            "Возможна проблема с подключением через API к сайту с курсом валют"
        )


def get_price_stocks_snp500() -> list:
    """Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API."""
    load_dotenv()
    api_stock = os.getenv("API-KEY_STOCK")
    user_stocks = reading_json_file(
        user_setting
    )[0]["user_stocks"]
    price_stocks = []

    try:
        logger.info("Попытка подключения через API к сайту со стоимостью акций")
        for stock in user_stocks:
            response = requests.get(
                f"https://api.twelvedata.com/price?symbol={stock}&apikey={api_stock}"
            )
            dict_result = response.json()
            price_element = {
                "stock": stock,
                "price": round(float(dict_result.get("price")), 2),
            }
            logger.info("Успешное подключение через API к сайту со стоимостью акций")
            price_stocks.append(price_element)

        return price_stocks
    except requests.exceptions.RequestException:
        logger.warning(
            "Возможна проблема с подключением через API к сайту со стоимостью акций"
        )


if __name__ == "__main__":
    # pass
    # print(reading_xlsx(dir_transactions_excel))
    print(get_price_stocks_snp500())
    print(exchange_rate())
