import sys
import inspect


class BaseDbException(Exception):
    """
    BaseException raised for errors in application without full stacktrace.
    Attributes: message - explanation of the error
    """
    def __init__(self, message):
        try:
            ln = sys.exc_info()[-1].tb_lineno
        except AttributeError:
            ln = inspect.currentframe().f_back.f_lineno
        self.args = f"{type(self).__name__} (line {ln}): {message}",
