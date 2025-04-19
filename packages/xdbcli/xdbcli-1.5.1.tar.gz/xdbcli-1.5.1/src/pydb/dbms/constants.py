from enum import Enum


class DBMS(str, Enum):
    MYSQL = 'mysql'
    MSSQL = 'mssql'
    ORACLE = 'oracle'
    POSTGRESQL = 'postgresql'

    def __str__(self):
        return self.value

    def __init__(self, dbms: str):
        self.dbms = dbms


if __name__ == "__main__":
    for el in DBMS:
        print(el)