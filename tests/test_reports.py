import json

import pandas as pd

from src.reports import decorator_with_args, spending_by_category


def test_decorator_with_args(lst_for_tests_csv_xlsx: list[dict]) -> None:
    @decorator_with_args(
        "C:/Users/111/PycharmProjects/coursework_1/tests/data/decorators_mistakes.json"
    )
    def test_spending_by_category() -> pd.DataFrame:
        """Функция тестирует декоратор"""
        data = [{"Сумма операции": -20000.0}]
        assert (
            spending_by_category(
                pd.DataFrame(lst_for_tests_csv_xlsx), "Переводы", "31.10.2021"
            ).to_dict("records")
            == data
        )
        return spending_by_category(
            pd.DataFrame(lst_for_tests_csv_xlsx), "Переводы", "31.10.2021"
        )

    result = test_spending_by_category()
    with open(
        "C:/Users/111/PycharmProjects/coursework_1/tests/data/decorators_mistakes.json",
        encoding="utf-8",
    ) as file:
        data_json = json.load(file)
    assert result.to_dict("records") == data_json
