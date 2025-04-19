from .mysql import MysqlConnectorBuilder
from .mssql import MssqlConnectorBuilder
from .oracle import OracleConnectorBuilder
from .postgresql import PostgresqlConnectorBuilder
from .arguments import DbArgumentParser
from .constants import DBMS


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


class DataBaseFactory(ObjectFactory):
    def get(self, **kwargs):
        parser = DbArgumentParser(kwargs.pop('connection'))
        kwargs.setdefault('arguments', parser)
        return self.create(parser.dbms, **kwargs)


database_factory = DataBaseFactory()
database_factory.register_builder(DBMS.MYSQL, MysqlConnectorBuilder())
database_factory.register_builder(DBMS.MSSQL, MssqlConnectorBuilder())
database_factory.register_builder(DBMS.ORACLE, OracleConnectorBuilder())
database_factory.register_builder(DBMS.POSTGRESQL, PostgresqlConnectorBuilder())
