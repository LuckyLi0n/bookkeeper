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
    expense_date: str = f'{datetime.now() : %Y-%m-%d}'
    comment: str = ''
    pk: int = 0
