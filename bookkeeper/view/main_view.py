"""Главное окно """

# pylint: disable= no-name-in-module, c-extension-no-member
# mypy: disable-error-code = attr-defined
# Ошибки связанные с Qt
from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget,\
    QGridLayout, QComboBox, QLineEdit, QPushButton

from bookkeeper.view.table_model import TableModel


class MainWindow(QtWidgets.QMainWindow):
    """Главное окно"""

    def __init__(self) -> None:
        super().__init__()

        self.item_model = None

        self.setWindowTitle("Программа для ведения бюджета")

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)
        self.amount_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)

        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)
        self.category_dropdown = QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.bottom_controls.addWidget(QLabel('Комментарий'), 2, 0)
        self.comment_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.comment_line_edit, 2, 1)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 3, 1)

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

    def set_category_dropdown(self, data) -> None:
        """Отвечает за выпадающий список категорий"""
        for obj in data:
            self.category_dropdown.addItem(obj.name, obj.pk)

    def on_expense_add_button_clicked(self, slot) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Добавить" """
        self.expense_add_button.clicked.connect(slot)

    def get_amount(self) -> float:
        """Возвращает введенную пользователем сумму"""
        return float(self.amount_line_edit.text())

    def get_comment(self) -> str:
        """Возвращает напечатанный пользователем комментарий"""
        return str(self.comment_line_edit.text())

    def get_selected_cat(self) -> int:
        """Возвращает выбранную категорию"""
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())
