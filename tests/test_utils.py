from datetime import datetime
from unittest.mock import mock_open, patch

import pytest

from src.utils import reading_json_file


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="""[{"user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}]""",
)
def test_valid_reading_json_file(mock_file: str) -> None:
    """Функция тестирует reading_json_file from src.utils на корректный файл с транзакциями"""
    transactions = reading_json_file("user_settings.json")
    assert transactions == [
        {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
        }
    ]


@patch("builtins.open", new_callable=mock_open, read_data='{"amount": 100}')
def test_not_a_list_reading_json_file(mock_file: str) -> None:
    """Функция тестирует reading_json_file from src.utils на некорректные данные (например, не список)"""
    not_a_list_transactions = reading_json_file("user_settings.json")
    assert not_a_list_transactions == []


@patch("builtins.open", side_effect=FileNotFoundError)
def test_file_not_found_reading_json_file(mock_file: str) -> None:
    """Функция тестирует reading_json_file from src.utils на случай, если файл не найден"""
    file_not_found_transactions = reading_json_file("user_settings.json")
    assert file_not_found_transactions == []
