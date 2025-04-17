class TenUtilsLibError(Exception):
    """
    Base exception class for all errors raised by the ten-utils library.

    This class is intended to be subclassed for specific error types.
    By creating a custom base exception, we allow users of the library
    to catch all related errors with a single except block if needed.

    Example:
        try:
            # some operation that might raise a library-specific error
            do_something()
        except TenUtilsLibError as e:
            handle_error(e)
    """
    pass