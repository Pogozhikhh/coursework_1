from src.services import investment_bank


def test_investment_bank_more_than_in_the_list(lst_for_tests_csv_xlsx: list) -> None:
    """Функция тестирует investment_bank по дате, которая есть в файле"""
    invest_count = investment_bank("2024-12", lst_for_tests_csv_xlsx, 100)
    assert invest_count == 406.55


def test_investment_bank_less_than_in_the_list(lst_for_tests_csv_xlsx: list) -> None:
    """Функция тестирует investment_bank по дате, которой нет в файле"""
    invest_count = investment_bank("2018-12", lst_for_tests_csv_xlsx, 100)
    assert invest_count == 0
