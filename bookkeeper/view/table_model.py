"""Таблица для использования в графическом интерфейсе"""

# pylint: disable = c-extension-no-member, invalid-name, unused-argument, no-name-in-module)
# mypy: disable-error-code = attr-defined
# Ошибки связанные с Qt и особенностями устройства QAbstractTableModel
from typing import Any
from PySide6 import QtCore
from PySide6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    """Таблица для показа пользователю сгенерированная из таблицы SQL"""
    def __init__(self, data) -> None:

        def col_name_to_rus(columns: list) -> list:
            names_dict = {'pk': 'ID', 'amount': 'Сумма', 'category': 'Категория',
                          'expense_date': 'Дата покупки', 'comment': 'Комментарий',
                          'budget': 'Бюджет', 'name': 'Название',
                          'parent': 'Родительская категория'}
            names = []
            for i in columns:
                names.append(names_dict.get(i))
            return names

        super().__init__()
        self._data = data
        self.header_names = col_name_to_rus(list(data[0].__dataclass_fields__.keys()))

    def headerData(self, section, orientation, role=Qt.DisplayRole) -> Any:
        """Подпись столбцов"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role) -> Any:
        """Обработка таблицы sql"""
        if role == Qt.DisplayRole:
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])
        return None

    def rowCount(self, index) -> int:
        """Определение количества строк в таблице"""
        return len(self._data)

    def columnCount(self, index) -> int:
        """Определение количества столбцов в таблице"""
        return len(self._data[0].__dataclass_fields__)
