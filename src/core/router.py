from typing_extensions import Callable


def action(*args, **kwargs) -> Callable:
    """Tool to add new action to API."""
    def wrapper(func) -> Callable:
        return func
    return wrapper
