# -*- coding: utf-8 -*-

from com.solver.game.common.GameLogger import create_logger

logger = create_logger()


def log_errors(f, name=None):
    """Decorator to log all errors from a method"""

    if name is None:
        name = f.func_name

    def wrapped(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result
        except:
            logger.exception(name)
            raise

    return wrapped
