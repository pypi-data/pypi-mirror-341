from .connector import UniDbConnector
from .connector import DatabaseError


class MssqlConnectorBuilder:
    def __init__(self):
        self._instance = None
        self._cfg = None

    def __call__(self, arguments, **kwargs):
        if not self._instance:
            self._instance = self.get_instance(arguments, **kwargs)
        return self._instance

    def get_instance(self, db_args, **kwargs):

        authentication_scheme = kwargs.get('authenticationScheme')

        if authentication_scheme == 'NTLM':
            db_args.options.append(f'authenticationScheme=NTLM')
            db_args.options.append(f'integratedSecurity=true')
            db_args.options.append(f'sslProtocol=TLS')
            db_args.options.append(f'trustServerCertificate=true')

            if '@' in db_args.user:
                user, domain = db_args.user.split('@')
                db_args.user = user
                db_args.options.append(f'domain={domain}')

        url = f"jdbc:sqlserver://;serverName={db_args.host};portNumber={db_args.port};databaseName={db_args.database}"

        cfg = dict(
            user=db_args.user,
            password=db_args.password,
            url=f"{url};{db_args.options_as_str()};",
        )

        cfg['driverJarFile'] = kwargs.get('driverJarFile')
        cfg['driverClass'] = kwargs.get('driverClass')

        self._cfg = cfg.copy()
        return MssqlConnector(self._cfg, **kwargs)


class MssqlConnector(UniDbConnector):
    """
    Mssql DataBase connector class.
    """

    def __init__(self, config: dict, **kwargs):
        super().__init__(config, **kwargs)

    def connect(self):
        """Connect to a Mssql database."""
        try:
            import jaydebeapi
            self._dbError = jaydebeapi.DatabaseError
        except ModuleNotFoundError:
            raise DatabaseError(message=f"ModuleNotFoundError: Driver for {self.__class__.__name__} not found!")

        try:
            self._connect = jaydebeapi.connect(
                self.config.get('driverClass'),
                self.config.get('url'),
                {'user': self.config.get('user'), 'password': self.config.get('password')},
                self.config.get('driverJarFile'),
            )
            self._connect.autocommit = self.autocommit
            return self._connect

        except self._dbError as Error:
            raise DatabaseError(message=f"Connection Error: {Error}")
