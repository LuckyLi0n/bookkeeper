"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0

    def convert_to_list(self):
        return[self.pk, self.amount, self.category, self.expense_date, self.added_date, self.comment]
