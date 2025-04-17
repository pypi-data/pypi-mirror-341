from pathlib import Path

from pydantic import BaseModel, field_validator


class EnvLoaderValuesValidator(BaseModel):
    """
    Validator for environment file loading configuration.

    This model ensures that the path to the environment file is provided
    and is properly cast to a `Path` object, even if passed as a string.

    Attributes:
        path_to_env_file (str | Path): The path to the `.env` file. Accepts
            both string and `Path` types. Will always be converted to `Path`.

    Example:
        EnvLoaderValuesValidator(path_to_env_file=".env")
    """

    path_to_env_file: str | Path

    @field_validator("path_to_env_file")
    def check_path_to_env_file(cls, value) -> Path:
        """
        Ensures that the value is a `Path` instance.

        Args:
            value (str | Path): The raw value passed to the `path_to_env_file` field.

        Returns:
            Path: A `Path` object representing the given file path.

        Raises:
            TypeError: This method does not explicitly raise, but could be extended
            to raise if value is of unsupported type.
        """
        if isinstance(value, str):
            return Path(value)

        return value

