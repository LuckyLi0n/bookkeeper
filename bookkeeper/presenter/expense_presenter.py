from bookkeeper.models.expense import Expense


class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.exp_data = [exp.convert_to_list() for exp in self.exp_repo.get_all()]
        self.cat_data = [cat.convert_to_list() for cat in self.cat_repo.get_all()]
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)

    def update_expense_data(self) -> None:
        self.exp_data = [exp.convert_to_list() for exp in self.exp_repo.get_all()]
        data = []
        for tup in self.exp_data:
            row = list(tup)
            for cat_tup in self.cat_data:
                if cat_tup[0] == row[2]:
                    row[2] = cat_tup[1]
                    break
            data.append(row)
        self.exp_data = data
        self.view.set_expense_table(self.exp_data)

    def show(self) -> None:
        self.view.show()
        self.update_expense_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        comment = self.view.get_comment()
        exp = Expense(int(amount), cat_pk, comment=comment)
        self.exp_repo.add(exp)
        self.update_expense_data()
