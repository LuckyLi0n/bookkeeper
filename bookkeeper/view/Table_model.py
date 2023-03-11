from PySide6 import QtCore


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):

        def col_name_to_rus(columns: list) -> list:
            names_dict = {'pk': 'ID', 'amount': 'Сумма', 'category': 'Категория', 'expense_date': 'Дата покупки',
                          'comment': 'Комментарий', 'budget': 'Бюджет'}
            names = []
            for i in columns:
                names.append(names_dict.get(i))
            return names

        super(TableModel, self).__init__()
        self._data = data
        self.header_names = col_name_to_rus(list(data[0].__dataclass_fields__.keys()))

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0].__dataclass_fields__)
