"""Таблица для использования в графическом интерфейсе"""

# pylint: disable = c-extension-no-member, invalid-name, unused-argument
# mypy: disable-error-code = attr-defined
# Ошибки связанные с Qt и особенностями устройства QAbstractTableModel
from PySide6 import QtCore
from typing import Any

class TableModel(QtCore.QAbstractTableModel):
    """Таблица для показа пользователю сгенерированная из таблицы SQL"""
    def __init__(self, data) -> None:

        def col_name_to_rus(columns: list) -> list:
            names_dict = {'pk': 'ID', 'amount': 'Сумма', 'category': 'Категория',
                          'expense_date': 'Дата покупки', 'comment': 'Комментарий',
                          'budget': 'Бюджет'}
            names = []
            for i in columns:
                names.append(names_dict.get(i))
            return names

        super().__init__()
        self._data = data
        self.header_names = col_name_to_rus(list(data[0].__dataclass_fields__.keys()))

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole) -> Any:
        """Подпись столбцов"""
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role) -> Any:
        """Обработка таблицы sql"""
        if role == QtCore.Qt.DisplayRole:
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])
        return None

    def rowCount(self, index) -> int:
        """Определение количества строк в таблице"""
        return len(self._data)

    def columnCount(self, index) -> int:
        """Определение количества столбцов в таблице"""
        return len(self._data[0].__dataclass_fields__)
