"""Главное окно """

# pylint: disable= no-name-in-module, c-extension-no-member
# mypy: disable-error-code = attr-defined
# Ошибки связанные с Qt
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget,\
    QGridLayout, QComboBox, QLineEdit, QPushButton

from bookkeeper.view.table_model import TableModel


class MainWindow(QtWidgets.QMainWindow):
    """Главное окно"""

    def __init__(self) -> None:
        super().__init__()

        self.item_model = None
        self.width = 600

        self.setWindowTitle("Программа для ведения бюджета")

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QLabel('Бюджет'))

        self.budget_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.budget_grid)

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)
        self.amount_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)

        self.bottom_controls.addWidget(QLabel('Дата покупки'), 1, 0)
        self.date_input = DateWidget()
        self.bottom_controls.addWidget(self.date_input, 1, 1)

        self.bottom_controls.addWidget(QLabel('Категория'), 2, 0)
        self.category_dropdown = QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 2, 1)

        self.bottom_controls.addWidget(QLabel('Комментарий'), 3, 0)
        self.comment_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.comment_line_edit, 3, 1)

        self.expense_change_button = QPushButton('Изменить')
        self.bottom_controls.addWidget(self.expense_change_button, 4, 0)
        self.expense_change_button.setToolTip(
            'Веди все параметры, потом выдели строку, '
            'которую нужно заменить и нажми эту кнопку\n'
            'Чтобы выделить строку нажми на ее номер')

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 4, 1)

        self.expense_delete_button = QPushButton('Удалить')
        self.bottom_controls.addWidget(self.expense_delete_button, 4, 2)
        self.expense_delete_button.setToolTip(
            'Выдели строки, которые хочешь удалить и нажми эту кнопку\n'
            'Чтобы выделить строки нажимай на их номера')

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data) -> None:
        """Создает таблицу расходов"""
        if data:
            self.item_model = TableModel(data)
            self.expenses_grid.setModel(self.item_model)
            self.expenses_grid.setColumnHidden(4, True)
            self.expenses_grid.setColumnWidth(1, 120)
            self.expenses_grid.setColumnWidth(3, 240)

    def set_budget_table(self, data) -> None:
        pass
        """Создает таблицу расходов"""
        if data:
            self.item_model = TableModel(data)
            self.budget_grid.setModel(self.item_model)
            self.budget_grid.setColumnHidden(3, True)
            for num in range(3):
                self.budget_grid.setColumnWidth(num, (self.width-40)//3)
                self.budget_grid.setRowHeight(1, 30)
            self.budget_grid.setMaximumHeight(120)
            self.setFixedSize(self.width, 600)

    def set_category_dropdown(self, data) -> None:
        """Отвечает за выпадающий список категорий"""
        for obj in data:
            self.category_dropdown.addItem(obj.name, obj.pk)

    def on_expense_add_button_clicked(self, slot) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Добавить" """
        self.expense_add_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot):
        """Отвечает за вызов определенной функции при нажатии кнопки "Удалить" """
        self.expense_delete_button.clicked.connect(slot)

    def on_expense_change_button_clicked(self, slot):
        """Отвечает за вызов определенной функции при нажатии кнопки "" """
        self.expense_change_button.clicked.connect(slot)

    def get_amount(self) -> float:
        """Возвращает введенную пользователем сумму"""
        return float(self.amount_line_edit.text())

    def get_comment(self) -> str:
        """Возвращает напечатанный пользователем комментарий"""
        return str(self.comment_line_edit.text())

    def get_selected_cat(self) -> int:
        """Возвращает выбранную категорию"""
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def get_selected_date(self) -> int:
        """Возвращает выбранную дату"""
        return self.date_input.dateTime().toPython()

    def __get_selected_row_indices(self) -> list[int]:
        """Возвращает индексы выбранных мышкой строк"""
        return list(set([qmi.row() for qmi in
                         self.expenses_grid.selectionModel().selection().indexes()]))

    def get_selected_expenses(self, data) -> list[int] | None:
        """Возвращает список pk объектов, находящихся в строках выделенных мышкой"""
        self.item_model = TableModel(data)
        idx = self.__get_selected_row_indices()
        if not idx:
            return None
        return [self.item_model._data[i].pk for i in idx]


class DateWidget(QtWidgets.QDateEdit):
    """
    Виджет выбора даты в виде календаря
    """
    def __init__(self, date: QtCore.QDate = QtCore.QDate.currentDate()) -> None:
        super().__init__(date)
        self.setCalendarPopup(True)
        self.setDisplayFormat('dd.MM.yyyy')
        calendar = self.calendarWidget()
        calendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        calendar.setGridVisible(True)
