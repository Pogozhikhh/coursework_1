from datetime import datetime
from unittest.mock import patch

import pytest

from src.views import each_card, day_time_now, top_transactions


@pytest.mark.parametrize(
    ("now_datetime", "expected_greeting"),
    [
        (datetime(2024, 1, 1, hour=6, minute=0), "Доброе утро"),
        (datetime(2024, 1, 1, hour=14, minute=0), "Добрый день"),
        (datetime(2024, 1, 1, hour=18, minute=0), "Добрый вечер"),
        (datetime(2024, 1, 1, hour=0, minute=0), "Доброй ночи"),
    ],
)
@patch("src.views.datetime")
def test_day_time_now(mocked_datetime, now_datetime, expected_greeting):
    mocked_datetime.now.return_value = now_datetime
    assert day_time_now() == expected_greeting


def test_top_transactions():
    expected = [
        {
            "date": "01.02.2021",
            "amount": 357.96,
            "category": "Супермаркеты",
            "description": "Магнит",
        },
        {
            "date": "01.02.2021",
            "amount": 99.0,
            "category": "Фастфуд",
            "description": "Pingvin Kofe I Chaj",
        },
        {
            "date": "01.02.2021",
            "amount": 96.0,
            "category": "Супермаркеты",
            "description": "Колхоз",
        },
        {
            "date": "01.02.2021",
            "amount": 30.0,
            "category": "Связь",
            "description": "Devajs Servis.",
        },
    ]
    assert (
        top_transactions(
            "C:/Users/111/PycharmProjects/coursework_1/data/operations.xlsx",
            "02.02.2021",
        )
        == expected
    )


def test_each_card():
    expected = [{"last_digits": "7197", "total_spent": 582.96, "cashback": 5.83}]
    assert (
        each_card(
            "C:/Users/111/PycharmProjects/coursework_1/data/operations.xlsx",
            "02.02.2021",
        )
        == expected
    )
