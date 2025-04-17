from functools import wraps
import inspect


def check_now_log_level(user_level: int):
    """
    A decorator that conditionally executes logging methods based on the current log level
    of the logger instance.

    This decorator compares the specified `user_level` of the log method
    (e.g., DEBUG=0, INFO=1, etc.) with the `level` attribute of the Logger instance.
    If the current log level is less than or equal to the method's level, the method executes.
    Otherwise, it is skipped.

    Additionally, this decorator injects the name of the calling function into the method's
    `kwargs` as `caller_name`, enabling the logger to display the source of the log message.

    Args:
        user_level (int): The severity level of the log method being decorated (0–4).

    Returns:
        Callable: The wrapped function, conditionally executed based on log level.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Access the Logger instance (self)
            self = args[0]
            now_level = getattr(self, "level", None)

            # Inspect the call stack to identify the function that called the logger
            frame = inspect.currentframe()
            caller_frame = frame.f_back
            caller_name = caller_frame.f_code.co_name

            # Inject the caller's name into kwargs for logger context
            kwargs["caller_name"] = caller_name

            # Compare the log level and conditionally execute
            if user_level >= now_level:
                return func(*args, **kwargs)

            else:
                return None

        return wrapper

    return decorator
