from pathlib import Path
from typing import Any
import os
import json

from dotenv import load_dotenv

from ten_utils.common.validators import EnvLoaderValuesValidator
from ten_utils.common.errors import (
    FailedLoadEnvVariables,
    FailedConvertTypeEnvVar,
    NotFoundNameEnvVar,
)
from ten_utils.common.singleton import Singleton


class EnvLoader(metaclass=Singleton):
    """
    A singleton-based environment variable loader and validator.

    This class loads environment variables from a given `.env` file path and
    casts them to specified types. It supports built-in types like str, int,
    float, bool, list, and tuple, with validation and error handling.

    Attributes:
        path_to_env_file (Path): Absolute path to the `.env` file.
    """

    def __init__(self, path_to_env_file: str | Path):
        """
        Initialize the environment loader and load the .env file.

        Args:
            path_to_env_file (str | Path):
                The path to the environment file.

        Raises:
            FailedLoadEnvVariables:
                If the environment file is not found or cannot be loaded.
        """
        loader_env_values = EnvLoaderValuesValidator(
            path_to_env_file=path_to_env_file,
        )

        self.path_to_env_file = loader_env_values.path_to_env_file
        load_result: bool = load_dotenv(dotenv_path=self.path_to_env_file)

        if not load_result:
            raise FailedLoadEnvVariables

    def load(self, name_env: str, type_env_var: type) -> Any:
        """
        Load and cast an environment variable to the specified type.

        Args:
            name_env (str):
                The name of the environment variable.
            type_env_var (type):
                The type to which the value should be cast.

        Returns:
            Any:
                The cast environment variable value.

        Raises:
            NotFoundNameEnvVar:
                If the environment variable is not found.
            FailedConvertTypeEnvVar:
                If the conversion fails or an invalid type is provided.
            ValueError:
                If `type_env_var` is None.
        """
        env_value: str | None = os.getenv(name_env)
        if env_value is None:
            raise NotFoundNameEnvVar(name_env=name_env)

        if type_env_var is None:
            raise ValueError("The 'type_env_var' argument cannot be 'None'")

        elif type_env_var is list or type_env_var is tuple:
            return self.__convert_var_to_list_or_tuple(
                env_value=env_value,
                type_env_var=type_env_var,
            )

        elif type_env_var is bool:
            return self.__convert_var_to_bool(
                env_value=env_value,
            )

        elif type_env_var is dict:
            return json.loads(env_value)

        try:
            return type_env_var(env_value)

        except ValueError:
            raise FailedConvertTypeEnvVar(
                convert_type=type_env_var,
                value=env_value,
            )

    @staticmethod
    def __convert_var_to_list_or_tuple(
        env_value: str,
        type_env_var: type,
    ) -> list | tuple:
        """
        Convert a comma-separated string to a list or tuple.

        Args:
            env_value (str):
                The environment variable value.
            type_env_var (type):
                Either `list` or `tuple`.

        Returns:
            list | tuple:
                Parsed list or tuple of values.

        Notes:
            Empty strings between commas are removed.
        """
        env_value = env_value.split(",")

        for key, value in enumerate(env_value):
            if value == "":
                del env_value[key]

        if type_env_var is tuple:
            return tuple(env_value)

        return env_value

    @staticmethod
    def __convert_var_to_bool(env_value: str) -> bool:
        """
        Convert a string representation of a boolean to a real boolean value.

        Args:
            env_value (str):
                The environment variable value.

        Returns:
            bool:
                True or False depending on the string content.

        Raises:
            FailedConvertTypeEnvVar:
                If the string does not represent a valid boolean.

        Accepted True values (case-insensitive):
            'true', 'yes', '1'

        Accepted False values (case-insensitive):
            'false', 'no', '0'
        """
        true_values = ["true", "yes", "1"]
        false_values = ["false", "no", "0"]

        value_normalized = str(env_value).lower().strip()

        if value_normalized in true_values:
            return True

        if value_normalized in false_values:
            return False

        raise FailedConvertTypeEnvVar(
            convert_type=bool,
            value=env_value,
        )
