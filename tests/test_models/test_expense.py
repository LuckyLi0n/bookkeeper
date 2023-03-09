from datetime import datetime

import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.expense import Expense


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    e = Expense(amount=100, category=1, expense_date=datetime.now(),
                added_date=datetime.now(), comment='test', pk=1)
    assert e.amount == 100
    assert e.category == 1


def test_create_brief():
    e = Expense(100, 1)
    assert e.amount == 100
    assert e.category == 1


def test_can_add_to_repo(repo):
    e = Expense(100, 1)
    pk = repo.add(e)
    assert e.pk == pk


def test_convert_to_list():
    amount = 100
    category = 1
    expense_date = datetime.now()
    added_date = datetime.now()
    comment = 'test'
    pk = 1
    e = Expense(amount=amount, category=category, expense_date=expense_date,
                added_date=added_date, comment=comment, pk=pk)
    assert e.convert_to_list() == [pk, amount, category, expense_date, added_date, comment]
