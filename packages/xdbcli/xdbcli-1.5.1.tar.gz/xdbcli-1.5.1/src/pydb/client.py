import cmd
import time
from prettytable import PrettyTable
from prettytable import from_db_cursor
from .dbms.connector import UniDbConnector


class CmdClient(cmd.Cmd):
    __DEFAULT_PROMPT = 'SQL> '
    __ONINPUT_PROMPT = '> '

    def __init__(self, db: UniDbConnector):
        super().__init__()
        self.prompt = self.__DEFAULT_PROMPT
        self.delimiter = '=' * 40
        self._buffer = ''
        self.db = db

        self.db.connect()

    def emptyline(self):
        pass

    def default(self, line: str) -> None:
        self.do_execute(query=line)

    def do_execute(self, query: str) -> None:
        if self._check_query(query):
            time_begin_execute = time.time()
            cursor = self.execute(query=self._buffer)
            self._clear_buffer()
            if cursor:
                table: PrettyTable = from_db_cursor(cursor)
                table.align = "l"
                time_of_execute = time.time() - time_begin_execute
                rows_count = len(table.rows) if len(table.rows) is not None else cursor.rowcount
                print(table)
                print(f'Rows: {rows_count}')
                print(f'Time: {time_of_execute:.2f}')

    def _check_query(self, line: str):
        if not line.endswith(';'):
            self._add_buffer(line)
            return False
        else:
            if self._buffer:
                self._add_buffer(line)
            else:
                self._buffer = line
            return True

    def _add_buffer(self, line: str):
        self.prompt = self.__ONINPUT_PROMPT
        self._buffer += ' ' + line + '\n'

    def _clear_buffer(self):
        self._buffer = ''
        self.prompt = self.__DEFAULT_PROMPT

    def help_execute(self):
        print(f'{self.delimiter}\nType: SELECT * FROM table;\n{self.delimiter}')

    def execute(self, query: str):
        """
        Method to fetchall data
        :param query: sql query to execute
        :return: List[tuple] of query results
        """

        try:
            cursor = self.db.execute(query=query)
            return cursor
        except Exception as Error:
            print(f'{self.delimiter}\nError: {Error}\n{self.delimiter}')

    def do_exit(self, line):
        print(line)
        print(f'{self.delimiter}\nGoodbye!\n{self.delimiter}')
        return True

    def help_exit(self):
        print(f'{self.delimiter}\nInput exit or Ctrl+C to quit\n{self.delimiter}')

    def close(self):
        self.do_exit(self.prompt)
