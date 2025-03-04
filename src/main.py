from pathlib import Path

from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import reading_xlsx
from src.views import views

current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir / "data" / "operations.xlsx"


def views_option() -> None:
    """Функция, которая выдает список транзакций по выбранной дате."""
    print(
        """Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Пропишите дату по которую хотите видеть данные о картах и затратах по ним и топ-5 транзакций по сумме платежа
в формате YYYY-MM-DD HH:MM:SS"""
    )
    date_answer = input("Пользователь: ")
    print(f"Программа: Для обработки выбран {date_answer}.")
    try:
        print(
            views(
                "C:/Users/111/PycharmProjects/coursework_1/data/operations.xlsx",
                date_answer,
            )
        )
    except KeyError:
        print("Программа: возможно вы написали дату не в том формате.")


def services_option() -> None:
    """Функция, которая выдает счет «Инвесткопилки»."""
    print(
        """Программа: Продолжим, теперь напишите месяц, до которого хотите посчитать инвестиции в формате %Y-%m."""
    )
    month_answer = input("Пользователь: ")
    print(f"Программа: Для обработки выбран {month_answer}.")
    print(
        """Программа: А теперь напишите комфортный порог округления: 10, 50 или 100 ₽."""
    )
    limit_answer = input("Пользователь: ")
    while limit_answer not in ["10", "50", "100"]:
        print(f'Программа: Такой порог "{limit_answer}" недоступен.')
        print("""Программа: Введите комфортный порог округления: 10, 50 или 100 ₽""")
        limit_answer = input("Пользователь: ")
    try:
        print(
            "Программа: Удалось бы сохранить "
            f"{investment_bank(month_answer,
                 reading_xlsx("C:/Users/111/PycharmProjects/coursework_1/data/operations.xlsx").to_dict('records'),
                               int(limit_answer))}"
        )
    except ValueError:
        print(
            "Программа: Возможно вы написали дату не в том формате или порог округления не тот"
        )


def reports_option() -> None:
    """Функция, которая выдает тратами по заданной категории за последние три месяца (от переданной даты)."""
    print(
        """Программа: Теперь напишите категорию, по которой хотите посмотреть траты."""
    )
    category_answer = input("Пользователь: ")
    print(f"Программа: Для обработки выбрана категория: {category_answer}.")
    print(
        """Программа: Также напишите дату, по которую мы будем смотреть траты(в целом
     за 3 месяца) в формате DD-MM-YYYY. Если ничего не введете, то траты будут отображены по текущую дату"""
    )
    end_date_answer = input("Пользователь: ")
    if end_date_answer != "":
        print(f"Программа: Для обработки выбран: {end_date_answer}.")
        try:
            print(
                spending_by_category(
                    reading_xlsx(
                        "C:/Users/111/PycharmProjects/coursework_1/data/operations.xlsx"
                    ),
                    category_answer,
                    end_date_answer,
                )
            )
        except KeyError:
            print("Программа: возможно вы написали дату не в том формате.")
    else:
        print(
            spending_by_category(
                reading_xlsx(
                    "C:/Users/111/PycharmProjects/coursework_1/data/operations.xlsx"
                ),
                category_answer,
            )
        )


def main() -> None:
    """Функция, которая отвечает за основную логику проекта
    и связывает функциональности между собой."""
    views_option()
    services_option()
    reports_option()


main()
