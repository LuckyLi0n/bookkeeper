""" Модуль реализующий внутреннюю логику и связывающий компоненты View и Model"""

#from datetime import datetime, timedelta

from bookkeeper.models.expense import Expense


class ExpensePresenter:
    """Связь компонентов View и Model"""
    def __init__(self, view, cat_repo, exp_repo, budget_repo) -> None:
        self.view = view
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.budget_repo = budget_repo
        self.exp_data = self.exp_repo.get_all()
        self.cat_data = self.cat_repo.get_all()
        self.budget_data = self.budget_repo.get_all()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)

    def update_expense_data(self) -> None:
        """Обновляет отображаемую таблицу расходов в соответствии с базой данных"""
        self.exp_data = self.exp_repo.get_all()
        if self.exp_data:
            for exp in self.exp_data:
                for cat in self.cat_data:
                    if cat.pk == exp.category:
                        exp.category = cat.name
                        break
        self.view.set_expense_table(self.exp_data)

    def update_budget_data(self) -> None:
        """Обновляет отображаемую таблицу бюджета в соответствии с базой данных"""
        pass
        self.view.set_budget_table(self.budget_data)

    def show(self) -> None:
        """Вызывает отображение главного окна"""
        self.view.show()
        self.update_expense_data()
        self.update_budget_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Добавить" добавляет в базу данных
        соответствующую запись и вызывает обновление таблиц
        """
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        comment = self.view.get_comment()
        date = self.view.get_selected_date()
        exp = Expense(int(amount), cat_pk, expense_date=date, comment=comment)
        self.exp_repo.add(exp)
        self.update_expense_data()
        self.update_budget_data()
