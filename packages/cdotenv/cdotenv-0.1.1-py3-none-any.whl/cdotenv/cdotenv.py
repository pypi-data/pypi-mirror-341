"""Module for loading and accessing environment variables from a .env file or StringIO.

This module provides functionality to load environment variables from a .env file
or StringIO object into os.environ and access them with type casting through a custom
Environ class. It supports type-hinted access to environment variables with automatic
conversion to specified types.

Public interfaces:
- load: Load environment variables from a file or StringIO.
- Environ: Base class for accessing environment variables with type casting.
- field: Decorator for defining environment variable fields with custom conversion.
"""

import os
from io import StringIO
from pathlib import Path
from typing import (
    Any,
    Callable,
    ClassVar,
    Iterable,
    Optional,
    Union,
    get_type_hints,
)

__all__ = ["load", "Environ", "field"]


def load(arg: Optional[Union[Path, StringIO]] = None) -> None:
    """Load environment variables from a .env file or StringIO into os.environ.

    Args:
        arg: Path to a .env file or a StringIO object containing environment
            variables in KEY=VALUE format. If None, defaults to '.env' in the
            current directory.

    Examples:
        >>> load()  # Loads from .env file
        >>> load(Path("custom.env"))  # Loads from custom.env
        >>> load(StringIO("KEY=VALUE\\n"))  # Loads from StringIO
    """
    if arg is None:
        arg = Path(".env")

    if isinstance(arg, Path):
        with arg.open("r") as env_file:
            _update_environ(env_file)
        return

    if isinstance(arg, StringIO):
        _update_environ(arg.readlines())
        return


class Environ:
    """Base class for accessing environment variables with type casting.

    Subclasses can define type-hinted class attributes to specify the expected
    types of environment variables. Accessing these attributes retrieves the
    corresponding environment variable and casts it to the annotated type.

    Raises:
        AttributeError: If the requested attribute is not defined in type hints.
        KeyError: If the environment variable is not found.
        ValueError: If the environment variable cannot be converted to the specified type.

    Examples:
        >>> class MyEnviron(Environ):
        ...     DEBUG: bool
        ...     TIMEOUT: int
        >>> env = MyEnviron()
        >>> env.DEBUG  # Returns True if os.environ["DEBUG"] is "true" or "1"
        >>> env.TIMEOUT  # Returns int(os.environ["TIMEOUT"])
    """

    autoloaded: bool
    prefix: str

    loaded: ClassVar[bool] = False

    __slots__ = ("autoloaded", "prefix")

    def __init__(
        self, /, *, prefix: str = "", autoloaded: bool = True
    ) -> None:
        """Initialize the Environ instance.

        Args:
            autoloaded: If True, automatically load environment variables from
                the default .env file upon instantiation.
        """
        if autoloaded and not Environ.loaded:
            load()
            Environ.loaded = True

        self.autoloaded = autoloaded
        self.prefix = prefix

    def __getattribute__(self, key: str, /) -> Any:
        prefix = object.__getattribute__(self, "prefix")
        key = f"{prefix}{key}"
        klass = object.__getattribute__(self, "__class__")
        type_hints = get_type_hints(klass)

        if key not in type_hints:
            raise AttributeError(
                f"'{klass.__name__}' object has no attribute '{key}'"
            )

        type_hint = type_hints[key]

        field = getattr(klass, key, type_hint)

        try:
            str_value = os.environ[key]
        except KeyError as error:
            raise ValueError(
                f"Environment variable '{key}' not found"
            ) from error

        try:
            value = field(str_value)
        except Exception as error:
            raise ValueError(
                f"Cannot convert '{str_value}' to {type_hint.__name__}"
            ) from error

        if not isinstance(value, type_hint):
            raise ValueError(
                f"Expected type '{type_hint.__name__}' for '{key}', "
                f"but got '{type(value).__name__}'"
            )

        return value


def field(call: Callable[[Any], Any]) -> Any:
    """Decorator for defining custom conversion logic for environment variables.

    Used in Environ subclasses to specify custom conversion functions for
    environment variable values. The decorated function is used to convert the
    string value before applying the type hint.

    Args:
        call: A callable that converts a string to the desired type.

    Returns:
        The callable itself, used as a marker for custom conversion.

    Examples:
        >>> class MyEnviron(Environ):
        ...     @field
        ...     def CUSTOM_FIELD(self, value: str) -> list:
        ...         return value.split(",")
        ...     CUSTOM_FIELD: list
        >>> env = MyEnviron()
        >>> env.CUSTOM_FIELD  # Converts os.environ["CUSTOM_FIELD"] to a list
    """
    return call


def _update_environ(lines: Iterable[str]) -> None:
    """Parse lines and update os.environ with KEY=VALUE pairs.

    Skips empty lines and comments (lines starting with '#').

    Args:
        lines: Iterable of strings in KEY=VALUE format.
    """
    for line in lines:
        if line.startswith("#") or not line.strip():
            continue
        key, value = line.strip().split("=", 1)
        os.environ[key] = value
