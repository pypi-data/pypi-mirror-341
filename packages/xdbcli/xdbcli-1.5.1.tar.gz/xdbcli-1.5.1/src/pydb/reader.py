import os
from .exceptions import BaseDbException


class FileReaderError(BaseDbException):
    """
    Exception raised for errors in Reader.
    """
    pass


class Reader:
    """
    Class to Read SQL-file
    """
    def __init__(self, filename: str):
        self._filename = filename
        self._extension = 'sql'
        self._statements = []

        self.__init_statements(value=filename)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value: str):
        self.__init_statements(value=value)

    def __init_statements(self, value: str):
        if value is None:
            raise FileReaderError(f'value - {value} is None!')

        if not os.path.isfile(value):
            raise FileReaderError(f'value - {value} is not a file!')

        if not os.path.exists(value):
            raise FileReaderError(f'value - {value} is not exists!')

        if not value.endswith(self._extension):
            raise FileReaderError(f'value - {value} has not valid extension - {self._extension}!')

        self._filename = value
        self._parse_sql()

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, value: str):
        self._extension = value

    @property
    def statements(self):
        return self._statements

    def _read_file(self, encoding='utf-8'):
        with open(self._filename, mode='r', encoding=encoding) as file:
            data = file.readlines()
        return data

    def _parse_sql(self):

        if len(self._statements) > 0:
            return self._statements

        data = self._read_file()
        DELIMITER = ';'
        stmt = ''

        for lineno, line in enumerate(data):
            if not line.strip():
                continue

            if line.startswith('--'):
                continue

            if 'DELIMITER' in line:
                DELIMITER = line.split()[1]
                continue

            if DELIMITER not in line:
                stmt += line.replace(DELIMITER, ';')
                continue

            if stmt:
                stmt += line
                self._statements.append(stmt.strip())
                stmt = ''
            else:
                self._statements.append(line.strip())
        return self._statements

    def __repr__(self):
        return '\n'.join(self._statements)

    def __len__(self):
        return len(self._statements)

    def __iter__(self):
        for stm in self._statements:
            yield stm
