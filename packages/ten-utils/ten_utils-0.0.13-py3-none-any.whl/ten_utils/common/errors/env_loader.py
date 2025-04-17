from typing import Any

from .base import TenUtilsLibError


class FailedLoadEnvVariables(TenUtilsLibError):
    """
    Raised when no environment variables could be loaded.

    This error typically indicates that:
    - The environment file was not found.
    - The environment file exists but is empty.

    Usage example:
        raise FailedLoadEnvVariables()
    """

    def __init__(self):
        super().__init__(
            "Not a single environment variable was loaded. "
            "Either the file with environment variables was "
            "not found or the file with environment variables is empty."
        )


class FailedConvertTypeEnvVar(TenUtilsLibError):
    """
    Raised when an environment variable fails to convert to the expected type.

    Args:
        convert_type (type): The target type to which the conversion was attempted.
        value (Any): The original value that failed to convert.

    This error usually occurs when parsing environment variables into
    typed configuration values.

    Usage example:
        raise FailedConvertTypeEnvVar(int, "abc")
    """

    def __init__(self, convert_type: type, value: Any):
        super().__init__(
            f"Converting an environment variable to type {convert_type!r} failed. "
            f"Most likely the value {value!r} cannot be converted to {convert_type!r} type."
        )


class NotFoundNameEnvVar(TenUtilsLibError):
    """
    Raised when a required environment variable name is missing.

    Args:
        name_env (str): The name of the environment variable that could not be found.

    This typically occurs when a specific environment variable is expected
    but not present in the current environment or configuration.

    Usage example:
        raise NotFoundNameEnvVar("DATABASE_URL")
    """

    def __init__(self, name_env: str):
        super().__init__(
            f"The environment variable name {name_env!r} was not found."
        )
