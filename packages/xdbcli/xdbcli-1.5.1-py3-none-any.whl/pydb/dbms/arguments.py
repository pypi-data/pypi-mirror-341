from urllib.parse import urlparse
from .constants import DBMS
from ..exceptions import BaseDbException


class DbArgumentError(BaseDbException):
    """
    Exception raised for errors in Arguments.
    """
    pass


class DbArgumentParser:
    def __init__(self, args: str = None):
        self._args = None
        self._dbms = None
        self._host = None
        self._port = None
        self._user = None
        self._password = None
        self._database = None
        self._options = None
        self.__init_args(args)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value: str):
        self.__init_args(value)

    def __init_args(self, value: str):
        if value is None:
            raise DbArgumentError(f'value - {value} is None!')

        self._args = self.__patched_urlparse(value)
        self._dbms = DBMS(self._args.scheme)
        self._host = self._args.hostname
        self._port = self._args.port
        self._user = self._args.username
        if self._password is None:
            self._password = self._args.password
        self._database, *self._options = self._args.path.lstrip("/").split(";")

    def __patched_urlparse(self, value: str):
        try:
            netloc = value.split(':')[2]
            self._password = netloc[:netloc.rfind('@')]
        except IndexError as Error:
            raise DbArgumentError(message=f'UrlParseError - {Error}')

        if ('[' in netloc and ']' not in netloc) or (']' in netloc and '[' not in netloc):
            monkey_pathed_password = 'password'
            value = value.replace(self._password, monkey_pathed_password)

        return urlparse(value)


    @property
    def dbms(self):
        return self._dbms

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value: str):
        self._user = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value: int):
        self._user = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value: str):
        self._user = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value: str):
        self._database = value


    @property
    def options(self):
        return self._options

    def __repr__(self):
        exclude = ["_args"]
        return str([f'{key.lstrip("_")}={value}' for key, value in vars(self).items() if key not in exclude])

    def options_as_dict(self):
        if self._options is not None:
            options_as_dict = {}
            for option in self._options:
                key, value = option.split("=")
                options_as_dict[key] = value
            return options_as_dict

    def options_as_str(self):
        if self._options is not None:
            return ";".join(self._options)
