from datetime import datetime

from rich.console import Console
from rich.text import Text

from ten_utils.common.constants import (
    LOGGER_LEVELS,
    LOGGER_INFO,
    LOGGER_FORMAT,
    CONSOLE_THEME,
)
from ten_utils.common.decorators import check_now_log_level
from ten_utils.log.config import LoggerConfig


class Logger:
    """
    A structured and stylized logger supporting colored console output, log level filtering,
    and optional file persistence.

    The Logger provides five logging levels:
        0 - DEBUG
        1 - INFO
        2 - WARNING
        3 - ERROR
        4 - CRITICAL

    Logging behavior (log level threshold and file saving) can be customized either globally via
    the LoggerConfig singleton, or per instance.

    Attributes:
        name (str | None): Optional identifier for the logger (e.g., module or class name).
        level (int): Minimum log level to display; messages below this level will be ignored.
        save_file (bool): Whether to persist log messages to a file (not yet implemented).
        console (Console): Rich Console instance used to print styled messages to the terminal.
    """

    logger_level = LOGGER_INFO

    def __init__(
        self,
        name: str | None = None,
        level: int | None = None,
        save_file: bool | None = None,
    ):
        """
        Creates a new Logger instance with optional overrides for logging level and file saving behavior.

        If no overrides are given, defaults are taken from the LoggerConfig singleton.

        Args:
            name (str | None): Optional label used to tag log output (e.g., a class or module name).
            level (int | None): Minimum severity level to log. Defaults to the global setting from LoggerConfig.
            save_file (bool | None): Whether to save logs to a file. Defaults to the global setting from LoggerConfig.
        """
        logger_config = LoggerConfig()

        self.name = name
        self.level = level if level is not None else logger_config.get_default_level_log()
        self.save_file = save_file if save_file is not None else logger_config.get_save_log_to_file()
        self.console = Console(theme=CONSOLE_THEME)

    @staticmethod
    def __get_caller_name(**kwargs) -> str:
        """
        Retrieves the caller name passed in through keyword arguments.

        Keyword Args:
            caller_name (str): A string indicating the source or context of the log.

        Returns:
            str: The caller name.
        """
        return kwargs["caller_name"]

    def __send(
            self,
            message: str,
            caller_name: str,
            now_log_level: int,
            additional_info: bool,
    ) -> None:
        """
        Formats and outputs a log message to the console, and optionally to a file.

        Args:
            message (str): The log message content.
            caller_name (str): Context or identifier of the log message source.
            now_log_level (int): Numeric representation of the log level (0 to 4).
            additional_info (bool): Whether to include timestamp, log level, logger name, and source in output.

        Side Effects:
            Prints the log message to the console.
            (Future) Writes the log message to a file if `save_file` is True.
        """
        arg_string = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            LOGGER_LEVELS[now_log_level].upper(),
            self.name,
            caller_name,
            message,
        )

        logger_format = (
            LOGGER_FORMAT if additional_info else LOGGER_FORMAT.split(":")[1].strip(" ")
        )

        message = logger_format.format(*arg_string)
        level_style = LOGGER_LEVELS.get(now_log_level, "info")

        self.console.print(Text(text=message, style=level_style))

        if self.save_file:
            pass  # Placeholder for file writing implementation

    @check_now_log_level(user_level=0)
    def debug(
            self,
            message: str,
            additional_info: bool = True,
            **kwargs,
    ) -> None:
        """
        Logs a debug-level message, typically used for detailed internal or diagnostic output.

        Args:
            message (str): The message to be logged.
            additional_info (bool, optional): If True, includes metadata like timestamp and source. Defaults to True.
            **kwargs: Must include 'caller_name' to tag the source of the message.
        """
        caller_name = self.__get_caller_name(**kwargs)
        self.__send(message, caller_name, 0, additional_info)

    @check_now_log_level(user_level=1)
    def info(
            self,
            message: str,
            additional_info: bool = True,
            **kwargs,
    ) -> None:
        """
        Logs an informational message used to report general application events or state.

        Args:
            message (str): The message to be logged.
            additional_info (bool, optional): If True, includes metadata like timestamp and source. Defaults to True.
            **kwargs: Must include 'caller_name' to tag the source of the message.
        """
        caller_name = self.__get_caller_name(**kwargs)
        self.__send(message, caller_name, 1, additional_info)

    @check_now_log_level(user_level=2)
    def warning(
            self,
            message: str,
            additional_info: bool = True,
            **kwargs,
    ) -> None:
        """
        Logs a warning message that flags unexpected behavior or potential issues.

        Args:
            message (str): The message to be logged.
            additional_info (bool, optional): If True, includes metadata like timestamp and source. Defaults to True.
            **kwargs: Must include 'caller_name' to tag the source of the message.
        """
        caller_name = self.__get_caller_name(**kwargs)
        self.__send(message, caller_name, 2, additional_info)

    @check_now_log_level(user_level=3)
    def error(
            self,
            message: str,
            additional_info: bool = True,
            **kwargs,
    ) -> None:
        """
        Logs an error message indicating a failure in a specific part of the application.

        Args:
            message (str): The message to be logged.
            additional_info (bool, optional): If True, includes metadata like timestamp and source. Defaults to True.
            **kwargs: Must include 'caller_name' to tag the source of the message.
        """
        caller_name = self.__get_caller_name(**kwargs)
        self.__send(message, caller_name, 3, additional_info)

    @check_now_log_level(user_level=4)
    def critical(
            self,
            message: str,
            additional_info: bool = True,
            **kwargs,
    ) -> None:
        """
        Logs a critical error message that may indicate unrecoverable failure. Exits the program afterward.

        Args:
            message (str): The message to be logged.
            additional_info (bool, optional): If True, includes metadata like timestamp and source. Defaults to True.
            **kwargs: Must include 'caller_name' to tag the source of the message.

        Side Effects:
            Prints message to console and exits the application with status code 1.
        """
        caller_name = self.__get_caller_name(**kwargs)
        self.__send(message, caller_name, 4, additional_info)
        exit(1)
