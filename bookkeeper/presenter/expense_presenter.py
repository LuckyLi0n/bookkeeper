from bookkeeper.models.expense import Expense


class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.exp_data = self.exp_repo.get_all()
        self.cat_data = self.cat_repo.get_all()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)

    def update_expense_data(self) -> None:
        """Обновляет отображаемую таблицу расходов в соответствии с базой данных"""
        self.exp_data = self.exp_repo.get_all()
        if self.exp_data:
            for e in self.exp_data:
                for c in self.cat_data:
                    if c.pk == e.category:
                        e.category = c.name
                        break
        self.view.set_expense_table(self.exp_data)

    def show(self) -> None:
        """Вызывает отображение главного окна"""
        self.view.show()
        self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        """При нажатии на кнопку "Добавить" добавляет в базу данных соответствующую запись"""
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        comment = self.view.get_comment()
        exp = Expense(int(amount), cat_pk, comment=comment)
        self.exp_repo.add(exp)
        self.update_expense_data()
