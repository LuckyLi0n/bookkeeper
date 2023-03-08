import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    b = Budget(amount=100, category=1, time=7, limit=1000, pk=1)
    assert b.amount == 100
    assert b.category == 1
    assert b.time == 7
    assert b.limit == 1000


def test_create_brief():
    b = Budget(100, 1, 7)
    assert b.amount == 100
    assert b.category == 1
    assert b.time == 7


def test_can_add_to_repo(repo):
    b = Budget(100, 1, 7)
    pk = repo.add(b)
    assert b.pk == pk
