from typing import Literal
from pydantic import BaseModel, StrictBool


class LoggerConfigValidator(BaseModel):
    """
    Validator for logger configuration values.

    This Pydantic model enforces type safety and constraints for logging configuration,
    ensuring consistent values across your application.

    Attributes:
        default_level_log (Literal[0, 1, 2, 3, 4]):
            The default logging level as an integer:
            - 0: DEBUG
            - 1: INFO
            - 2: WARNING
            - 3: ERROR
            - 4: CRITICAL
            This field only accepts one of these five literal values.

        save_log_to_file (StrictBool):
            A flag indicating whether logs should also be saved to a file in addition to the console.

    Example:
        LoggerConfigValidator(default_level_log=1, save_log_to_file=True)
    """

    default_level_log: Literal[0, 1, 2, 3, 4]
    save_log_to_file: StrictBool
