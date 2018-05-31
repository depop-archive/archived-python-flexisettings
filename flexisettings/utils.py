import os
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Generator  # noqa

from configloader import ConfigLoader

from flexisettings import Settings  # noqa


class OverrideSettings(object):

    def __init__(self, settings_obj, **kwargs):
        # type: (Settings, **str) -> None
        self._settings = settings_obj
        self.overrides = kwargs
        self.__old = None

    def __call__(self, f):
        # type: (Callable) -> Callable
        @wraps(f)
        def decorated(*args, **kwargs):
            with self:
                return f(*args, **kwargs)
        return decorated

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def enable(self):
        self.__old = ConfigLoader(self._settings.copy())
        new = ConfigLoader(self._settings.copy())
        new.update(self.overrides)
        self._settings._replace_wrapped(new)

    def disable(self):
        self._settings._replace_wrapped(self.__old)


override_settings = OverrideSettings


@contextmanager
def override_environment(settings, **kwargs):
    # type: (Settings, **str) -> Generator
    """
    Override env vars and reload the Settings object

    NOTE:
    Obviously this context has to be in place before you import any
    module which reads env values at import time.

    NOTE:
    The values in `kwargs` must be strings else you will get a cryptic:

        TypeError: execve() arg 3 contains a non-string value
    """
    old_env = os.environ.copy()
    os.environ.update(kwargs)

    settings._reload()

    try:
        yield
    except Exception:
        raise
    finally:
        for key in kwargs.keys():
            del os.environ[key]
        os.environ.update(old_env)

        settings._reload()
