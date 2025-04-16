from typing import Callable
from .log_decorator import LogDecorator
from .logger import Logger

class LogWrapper:
    def __init__(self, decorator: LogDecorator, logger: Logger):
        """
        Wraps both the logger and its associated decorator.

        :param decorator: LoggingDecorator instance for decorating functions.
        :param logger: Actual Python logger instance for logging messages directly.
        """
        self._decorator = decorator
        self._logger = logger

    def __call__(self, func: Callable):
        """
        Enables using this object as a decorator.

        :param func: The function to wrap.
        :return: Decorated function.
        """
        return self._decorator(func)

    def __getattr__(self, name: str):
        """
        Delegate everything else to the underlying Logger
        or the logging.Logger instance based on the attribute name.

        e.g., log.logger.info(...), log.logger.warning(...)

        :param name: Attribute or method name.
        :return: Logger method or property.
        """
        if any(keyword in name for keyword in ("context", "async", "get_logger")):
            return getattr(self._logger, name)
        else:
            return getattr(self._logger.get_logger(), name)
