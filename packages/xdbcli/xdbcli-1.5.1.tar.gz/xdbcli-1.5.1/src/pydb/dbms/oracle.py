import os
import sys
from .connector import UniDbConnector
from .connector import DatabaseError


class OracleConnectorBuilder:
    def __init__(self):
        self._instance = None
        self._cfg = None

    def __call__(self, arguments, **kwargs):
        if not self._instance:
            self._instance = self.get_instance(arguments, **kwargs)
        return self._instance

    def get_instance(self, db_args, **kwargs):

        dsn = f'{db_args.user}/{db_args.password}@{db_args.host}:{db_args.port}/{db_args.database}'
        cfg = dict(
            dsn=dsn,
        )
        options = db_args.options_as_dict()

        thin_mode = kwargs.get('thin_mode')
        cfg['thin_mode'] = thin_mode

        lib_dir = kwargs.get('lib_dir')
        if thin_mode is False and lib_dir is None:
            if sys.platform.startswith("linux"):
                lib_dir = os.environ.get("LD_LIBRARY_PATH")
            elif sys.platform.startswith("win32"):
                lib_dir = os.environ.get("ORACLE_HOME")

        cfg['lib_dir'] = lib_dir
        self._cfg = dict(cfg, **options)

        return OracleConnector(self._cfg, **kwargs)


class OracleConnector(UniDbConnector):
    """
    Oracle DataBase connector class.
    """

    def __init__(self, config: dict, **kwargs):
        super().__init__(config, **kwargs)
        self.thin_mode = config.pop('thin_mode')

    def connect(self):
        """Connect to a Oracle database."""

        try:
            import oracledb
            self._dbError = oracledb.DatabaseError

            lib_dir = self.config.pop('lib_dir', None)
            if self.thin_mode is False and lib_dir is not None:
                oracledb.init_oracle_client(lib_dir=lib_dir)
            elif self.thin_mode is False and lib_dir is None:
                oracledb.init_oracle_client()

        except ModuleNotFoundError:
            raise DatabaseError(message=f"ModuleNotFoundError: Driver for {self.__class__.__name__} not found!")

        except Exception as Error:
            raise DatabaseError(message=f"Exception: Instance client for {self.__class__.__name__} not found!\n{Error}")

        try:
            self._connect = oracledb.connect(**self.config, encoding='UTF-8')
            self._connect.autocommit = self.autocommit
            return self._connect

        except oracledb.DatabaseError as Error:
            raise DatabaseError(message=f"Connection Error: {Error}")

    def execute(self, query: str, params: tuple = None):
        query = query.strip("\n").strip(";")  # FIX - ORA-00911: invalid character
        return super().execute(query=query, params=params)

