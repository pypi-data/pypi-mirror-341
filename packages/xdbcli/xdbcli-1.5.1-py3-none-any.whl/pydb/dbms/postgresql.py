from .connector import UniDbConnector
from .connector import DatabaseError


class PostgresqlConnectorBuilder:
    def __init__(self):
        self._instance = None
        self._cfg = None

    def __call__(self, arguments, **kwargs):
        if not self._instance:
            self._instance = self.get_instance(arguments, **kwargs)
        return self._instance

    def get_instance(self, db_args, **kwargs):

        cfg = dict(
            host=db_args.host,
            port=db_args.port,
            user=db_args.user,
            password=db_args.password,
            database=db_args.database,
        )

        options = db_args.options_as_dict()
        self._cfg = dict(cfg, **options)

        return PostgresqlConnector(self._cfg, **kwargs)

class PostgresqlConnector(UniDbConnector):
    """
    Postgresql DataBase connector class.
    """
    def __init__(self, config: dict, **kwargs):
        super().__init__(config, **kwargs)

    def connect(self):
        """Connect to a Postgres database."""

        try:
            import psycopg2
            self._dbError = psycopg2.DatabaseError
        except ModuleNotFoundError:
            raise DatabaseError(message=f"ModuleNotFoundError: Driver for {self.__class__.__name__} not found!")

        try:
            self._connect = psycopg2.connect(**self.config)
            self._connect.autocommit = self.autocommit
            return self._connect
        except psycopg2.DatabaseError as Error:
            raise DatabaseError(message=f"Connection Error: {Error}")
