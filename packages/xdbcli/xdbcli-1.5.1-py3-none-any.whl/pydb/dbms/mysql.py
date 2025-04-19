from .connector import UniDbConnector
from .connector import DatabaseError


class MysqlConnectorBuilder:
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

        return MysqlConnector(self._cfg, **kwargs)


class MysqlConnector(UniDbConnector):
    """
    Mysql DataBase connector class.
    """

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

    def connect(self):
        """Connect to a Mysql database."""
        try:
            import pymysql
            self._dbError = pymysql.DatabaseError
        except ModuleNotFoundError:
            raise DatabaseError(message=f"ModuleNotFoundError: Driver for {self.__class__.__name__} not found!")

        try:
            self._connect = pymysql.connect(**self.config)
            self._connect.autocommit = self.autocommit
            return self._connect
        except pymysql.DatabaseError as Error:
            raise DatabaseError(message=f"Connection Error: {Error}")
