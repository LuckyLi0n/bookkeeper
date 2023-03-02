"""
Описан класс, представляющий бюджет.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Budget:
    """
    Бюджет на определенный промежуток времени для категории товаров.
    amount - сумма
    category - id категории расходов
    time - промежуток времени в днях
    pk - id записи в базе данных
    """
    amount: int
    category: int
    time: int
    pk: int = 0
