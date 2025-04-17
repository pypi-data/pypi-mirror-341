from typing import Literal

from ten_utils.common.singleton import Singleton
from ten_utils.common.validators import LoggerConfigValidator


class LoggerConfig(metaclass=Singleton):
    """
    Singleton configuration class for controlling logger behavior globally.

    This class provides centralized control over:
        - The default logging level.
        - Whether logs should be saved to a file.

    It ensures that any changes made to the logging configuration are
    reflected across all parts of the application using this config.
    """

    def __init__(self):
        """
        Initializes the default configuration for the logger.

        Default values:
            - Log level: INFO (1)
            - Save logs to file: False
        """
        logger_config_values = LoggerConfigValidator(
            default_level_log=1,
            save_log_to_file=False,
        )

        self.__default_level_log: Literal[0, 1, 2, 3, 4] = logger_config_values.default_level_log
        self.__save_log_to_file: bool = logger_config_values.save_log_to_file

    def get_default_level_log(self) -> Literal[0, 1, 2, 3, 4]:
        """
        Returns the current default log level.

        Returns:
            Literal[0, 1, 2, 3, 4]: The default log level (0=DEBUG, ..., 4=CRITICAL).
        """
        return self.__default_level_log

    def get_save_log_to_file(self) -> bool:
        """
        Returns whether log messages should be saved to a file.

        Returns:
            bool: True if logs should be saved to a file, False otherwise.
        """
        return self.__save_log_to_file

    def set_default_level_log(self, value: Literal[0, 1, 2, 3, 4]) -> None:
        """
        Sets the default logging level for all Logger instances
        that do not override it explicitly.

        Args:
            value (Literal[0, 1, 2, 3, 4]): New default log level.

        Raises:
            ValueError: If the value is invalid (validation handled by the validator).
        """
        logger_config_values = LoggerConfigValidator(
            default_level_log=value,
            save_log_to_file=self.__save_log_to_file,
        )

        self.__default_level_log = logger_config_values.default_level_log

    def set_save_log_to_file(self, value: bool) -> None:
        """
        Sets whether logs should be written to a file.

        Args:
            value (bool): True to enable file logging, False to disable it.

        Raises:
            ValueError: If the value is not a boolean (validated externally).
        """
        logger_config_values = LoggerConfigValidator(
            default_level_log=self.__default_level_log,
            save_log_to_file=value,
        )

        self.__save_log_to_file = logger_config_values.save_log_to_file
