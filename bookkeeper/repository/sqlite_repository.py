"""
Модуль описывает репозиторий, работающий в базе данных SQLite
"""

import sqlite3

from inspect import get_annotations

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий c базой данных SQLite и хранящий в ней данные.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({p})', values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'SELECT * FROM {self.table_name} ' + f'WHERE ROWID=={pk}'
            )
            res = cur.fetchall()
        con.close()
        return res  # TODO: исправить тип возвращаемого объекта

    def get_all(self, where: dict[str, any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            if where is None:
                cur.execute(
                    f'SELECT * FROM {self.table_name}'
                )
                res = cur.fetchall()
            else:
                pass    # TODO: добавить блок WHERE
        con.close()
        return res

    def update(self, obj: T) -> None:
        fields = ", ".join([f"{f}" for f in self.fields.keys()])
        values = [getattr(obj, f) for f in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'UPDATE {self.table_name} SET {fields} ' + f'WHERE ROWID=={obj.pk}', values
            )
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'DELETE FROM  {self.table_name} ' + f'WHERE ROWID=={pk}'
            )
            # TODO: рассмотреть возможные ошибки delete
        con.close()
