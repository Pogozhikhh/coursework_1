import logging
import math
import os
from typing import Any

import pandas as pd

from src.utils import df_to_transactions

path_file = os.path.dirname(os.path.abspath(__file__))

rel_file_path = os.path.join(path_file, "../logs/services.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def investment_bank(
    month: str, transactions: list[dict[str, Any]], limit: int
) -> float:
    """Функция, которая позволяет задавать комфортный порог округления: 10, 50 или 100 ₽.
    Траты будут округляться, и разница между фактической суммой трат по карте
     и суммой округления будет попадать на счет «Инвесткопилки»."""
    num = 0
    transactions = df_to_transactions(transactions)
    for i in transactions:
        if pd.to_datetime(i["Дата операции"]) < pd.to_datetime(month, format="%Y-%m"):
            num += math.ceil(abs(i["Сумма операции"]) / limit) * limit - abs(
                i["Сумма операции"]
            )
    return round(num, 2)


if __name__ == "__main__":
    pass
