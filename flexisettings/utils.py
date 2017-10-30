from functools import wraps
from typing import Callable  # noqa

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
