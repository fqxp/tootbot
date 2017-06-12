from functools import wraps
import logging
import traceback


def failsafe(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            logging.error(traceback.format_exc())

    return wrapper
