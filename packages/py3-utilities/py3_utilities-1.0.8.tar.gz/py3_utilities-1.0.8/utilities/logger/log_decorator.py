import logging
import functools
import time
import inspect
import traceback

from typing import Callable, Any, Union, Optional, List, TypeVar, ParamSpec

from .logger import Logger

P = ParamSpec("P")
R = TypeVar("R")


class LogDecorator:
    def __init__(
        self,
        logger: Union[logging.Logger, Logger],
        raise_exception: bool = True,
        log_level: int = logging.INFO,
        max_log_length: int = 500,
        sensitive_params: Optional[List[str]] = None,
        default_return: Any = None,
        log_arguments: bool = False,
        tag: Optional[str] = None,
        warn_duration: Optional[float] = None,
        log_stack: bool = False,
        log_return: bool = False,
        log_execution_time: bool = False
    ) -> None:
        """
        Initializes the logging decorator with configuration.

        :param logger: Logger instance to be used.
        :param raise_exception: Whether to re-raise exceptions after logging.
        :param log_level: Logging level for messages.
        :param max_log_length: Max characters to show per argument/return in logs.
        :param sensitive_params: List of argument names to be masked.
        :param default_return: Return value if an exception occurs and not re-raised.
        :param log_arguments: Whether to log function arguments.
        :param tag: Optional tag for log message prefixing.
        :param warn_duration: Threshold (in seconds) for performance warnings.
        :param log_stack: Whether to include call stack in logs.
        :param log_return: Whether to include return value in logs.
        :param log_execution_time: Whether to include function execution time in logs.
        """
        if isinstance(logger, Logger):
            self.logger = logger.get_logger()
        elif logger:
            self.logger = logger
        else:
            raise ValueError("Logger cannot be None")

        self.raise_exception = raise_exception
        self.log_level = log_level
        self.max_log_length = max_log_length
        self.sensitive_params = set(sensitive_params or [])
        self.default_return = default_return
        self.tag = f"[{tag}] " if tag else ""
        self.warn_duration = warn_duration
        self.log_arguments = log_arguments
        self.log_stack = log_stack
        self.log_return = log_return
        self.log_execution_time = log_execution_time

    def _truncate(self, value: Any) -> str:
        """
        Truncates a string representation of a value if it exceeds max_log_length.

        :param value: Value to be truncated.
        :return: Truncated string.
        """
        try:
            text = str(value)
        except Exception:
            text = repr(value)
        return text if len(text) <= self.max_log_length else text[:self.max_log_length] + " ... [TRUNCATED]"

    def _get_call_stack(self) -> str:
        """
        Retrieves a trimmed call stack for logging.

        :return: Formatted call stack string.
        """
        stack = traceback.format_stack()
        trimmed = stack[:-3]  # remove decorator's own frames

        formatted = []
        for index, element in enumerate(trimmed):
            parts = element.split("\n")
            formatted.append(f"\t{index+1}. - `{parts[1].lstrip()}` (Call location: `{parts[0].lstrip()}`)")

        return "\n".join(formatted)

    def _format_args(self, func: Callable[P, R], args: tuple, kwargs: dict) -> tuple[str, str]:
        """
        Formats positional and keyword arguments for logging.

        :param func: Function whose arguments are to be logged.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: Tuple of formatted positional and keyword argument strings.
        """
        try:
            bound = inspect.signature(func).bind(*args, **kwargs)
            bound.apply_defaults()
        except Exception:
            return "<unable to parse args>", "<unable to parse kwargs>"

        args_strs = []
        kwargs_strs = []

        for name, value in bound.arguments.items():
            val = '[FILTERED]' if name in self.sensitive_params else self._truncate(value)
            entry = f"{name}: `{val}`"
            if name in kwargs:
                kwargs_strs.append(entry)
            else:
                args_strs.append(entry)

        args_str = "\n" + "\n".join(f"Positional parameter {line}" for line in args_strs) if args_strs else ""
        kwargs_str = "\n" + "\n".join(f"Keyword parameter {line}" for line in kwargs_strs) if kwargs_strs else ""
        return args_str, kwargs_str

    def _log_sync(self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Logs a synchronous function's call, arguments, return value, and duration.

        :param func: Synchronous function to log.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: Result of the function call or default return value.
        """
        func_name = f"{func.__module__}.{func.__name__}"

        if self.logger.isEnabledFor(self.log_level):
            if self.log_arguments:
                args_str, kwargs_str = self._format_args(func, args, kwargs)
                self.logger.log(self.log_level, f"{self.tag}Function `{func_name}` called.{args_str}{kwargs_str}")
            else:
                self.logger.log(self.log_level, f"{self.tag}Function `{func_name}` called.")

            if self.log_stack:
                self.logger.debug(f"{self.tag}Call stack for `{func_name}`:\n{self._get_call_stack()}")

        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time

            if self.log_execution_time:
                self.logger.log(self.log_level, f"{self.tag}Function `{func_name}` returned after {elapsed:.2f} seconds.")

            if self.warn_duration and elapsed > self.warn_duration:
                self.logger.warning(f"{self.tag}Function `{func_name}` exceeded {self.warn_duration} seconds.")

            if self.log_return:
                self.logger.log(self.log_level, f"{self.tag}Return value: `{self._truncate(result)}`")

            return result
        except Exception as e:
            self.logger.critical(f"{self.tag}Exception in `{func_name}`: {type(e).__name__}: {str(e)}", exc_info=True)
            self.logger.debug(f"{self.tag}Call stack at exception in `{func_name}`:\n{self._get_call_stack()}")

            if self.raise_exception:
                raise

            return self.default_return

    async def _log_async(self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Logs an asynchronous function's call, arguments, return value, and duration.

        :param func: Asynchronous function to log.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: Result of the function call or default return value.
        """
        func_name = f"{func.__module__}.{func.__name__}"

        if self.logger.isEnabledFor(self.log_level):
            if self.log_arguments:
                args_str, kwargs_str = self._format_args(func, args, kwargs)
                self.logger.log(self.log_level, f"{self.tag}<Async> Function `{func_name}` called.{args_str}{kwargs_str}")
            else:
                self.logger.log(self.log_level, f"{self.tag}<Async> Function `{func_name}` called.")

            if self.log_stack:
                self.logger.debug(f"{self.tag}Call stack for `{func_name}`:\n{self._get_call_stack()}")

        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            elapsed = time.time() - start_time

            if self.log_execution_time:
                self.logger.log(self.log_level, f"{self.tag}Function `{func_name}` returned after {elapsed:.2f} seconds.")

            if self.warn_duration and elapsed > self.warn_duration:
                self.logger.warning(f"{self.tag}Function `{func_name}` exceeded {self.warn_duration} seconds.")

            if self.log_return:
                self.logger.log(self.log_level, f"{self.tag}Return value: `{self._truncate(result)}`")

            return result
        except Exception as e:
            self.logger.critical(f"{self.tag}Exception in `{func_name}`: {type(e).__name__}: {str(e)}", exc_info=True)
            self.logger.debug(f"{self.tag}Call stack at exception in `{func_name}`:\n{self._get_call_stack()}")
            
            if self.raise_exception:
                raise

            return self.default_return

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """
        Enables using this object as a decorator.

        :param func: The function to wrap.
        :return: Decorated function.
        """
        @functools.wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return await self._log_async(func, *args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return self._log_sync(func, *args, **kwargs)

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
