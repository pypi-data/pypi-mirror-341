from typing import List, Optional, Tuple
from abc import ABC, abstractmethod
from ..exceptions import BaseDbException


class DatabaseError(BaseDbException):
    """
    Exception raised for errors in DataBase Driver.
    """
    pass


class ExecutionResponse:
    """
    Class that is returned by execute() method of a DataBaseConnector class.
    :param result: Optional, return List[Dict] rows if success is True
    :param header: Optional, return List[Dict] rows headers if success is True
    :param count: Optional, return count() number of execute() results
    """

    def __init__(self,
                 result: Optional[List[Tuple[str, ...]]] = None,
                 header: Optional[Tuple[str, ...]] = None,
                 count: Optional[int] = None):
        self.result = result
        self.header = header
        self.count = count

    def __repr__(self):
        return self.result


class UniDbConnector(ABC):
    """
    Abstract DataBase connector class.
    """

    def __init__(self, config: dict, **kwargs):
        """
        param config: DbArgumentParser instance.
        """
        self.config: dict = config
        self.autocommit = kwargs.get('autocommit', True)
        self._connect = None
        self._dbError = Exception

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connect.close()

    def execute(self, query: str, params: tuple = None):
        """
        Method to execute sql query
        :raise DatabaseError
        """

        if self._connect is None:
            self._connect = self.connect()

        try:
            cursor = self._connect.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        except self._dbError as Error:
            raise DatabaseError(message=f"Execution Error: {Error}")
        return cursor

    def fetchmany(self, query: str, params: tuple = None, size=10000) -> tuple:
        """
        Method to fetchmany data
        :param query: sql query to execute
        :param params: params in where clause
        :param size: count rows to return
        :return: yield tuple of query results
        """
        cursor = self.execute(query=query, params=params)
        while True:
            results = cursor.fetchmany(size)
            if not results:
                break
            yield results

    def fetchmany_er(self, query: str, params: tuple = None, size=10000) -> ExecutionResponse:
        """
        Special method to fetchmany ExecutionResponse instance
        :param query: sql query to execute
        :param params: params in where clause
        :param size: count rows to return
        :return: yield ExecutionResponse of query results
        """
        cursor = self.execute(query=query, params=params)
        while True:
            results = cursor.fetchmany(size)
            if not results:
                break
            header = tuple(desc[0] for desc in cursor.description)
            yield ExecutionResponse(result=results, header=header, count=cursor.rowcount)

    def fetchall(self, query: str, params: tuple = None) -> List[tuple]:
        """
        Method to fetchall data
        :param query: sql query to execute
        :param params: params in where clause
        :return: List[tuple] of query results
        """
        cursor = self.execute(query=query, params=params)
        result = [row for row in cursor.fetchall()]
        return result

    def fetchall_er(self, query: str, params: tuple = None) -> List[ExecutionResponse]:
        """
        Special method to fetchall ExecutionResponse instance
        :param query: sql query to execute
        :param params: params in where clause
        :return: List[ExecutionResponse] of query results
        """
        cursor = self.execute(query=query, params=params)
        header = tuple(desc[0] for desc in cursor.description)
        result = [ExecutionResponse(result=row, header=header, count=cursor.rowcount) for row in cursor.fetchall()]
        return result



