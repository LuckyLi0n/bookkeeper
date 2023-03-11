"""Модуль запуска программы"""

# pylint: disable= no-name-in-module
# Ошибки связанные с Qt
import sys
from PySide6.QtWidgets import QApplication

from bookkeeper.view.main_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree


DB_NAME = 'test4.db'

if __name__ == '__main__':

    app = QApplication(sys.argv)

    view = MainWindow()

    category_repo = SQLiteRepository[Category](DB_NAME, Category)
    expense_repo = SQLiteRepository[Expense](DB_NAME, Expense)
    budget_repo = SQLiteRepository[Budget](DB_NAME, Budget)

    if not category_repo.get_all():
        cats = '''
                продукты
                    мясо
                        сырое мясо
                        мясные продукты
                    сладости
                    хлеб
                    напитки
                        кофе
                        чай
                        сок
                        вода
                развлечения
                    кино
                    театр
                    концерт
                    ресторан
                транспорт
                    бензин
                    метро
                    такси
                    билеты
                книги
                одежда
                товары для дома
                лекарства
                '''.splitlines()
        Category.create_from_tree(read_tree(cats), category_repo)

    window = ExpensePresenter(view, category_repo, expense_repo)
    window.show()
    app.exec()
