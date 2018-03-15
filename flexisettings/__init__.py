from importlib import import_module

import six
from six.moves import reload_module
from typing import Optional, Union  # noqa

from configloader import ConfigLoader
from wrapt import ObjectProxy

"""
Usage:

    from flexisettings.conf import settings

There are two important env vars:

    `<inital_namespace>_CONFIG_NAMESPACE`
        Sets the prefix used for loading further config values from env
        and config file. Set when instantiating the `Settings` object.
    `<inital_namespace>_APP_CONFIG`
        Import path to a python object to load futher config values from.
        Defaults to None. e.g. 'django.conf.settings' or 'celeryconfig'.

Although we can load further keys from the env, now prefixed using our
custom namespace, by preference all further keys should be loaded from a
python obj because all values loaded from env will be strings, there is no
way to automatically type cast them.

Keys in the config obj must be prefixed with the namespace, but will be
provided in `settings` without the prefix.

e.g. if you set your env to:

    MYAPP_CONFIG_NAMESPACE=MYAPP_EVENTS
    MYAPP_APP_CONFIG=django.conf.settings

and in your Django settings you have:

    MYAPP_EVENTS_SERIALIZER = 'json'

then:

    from event_consumer.conf import settings

    print(settings.SERIALIZER)
    > json
"""

if six.PY2:
    import_error_cls = ImportError
else:
    import_error_cls = ModuleNotFoundError  # noqa


class Settings(ObjectProxy):

    def __init__(self, initial_namespace=None, defaults=None):
        # type: (Optional[str], Optional[str]) -> None
        self._self_initial_namespace = initial_namespace
        self._self_defaults = defaults
        config = _load_config(initial_namespace, defaults)
        super(Settings, self).__init__(config)

    def __dir__(self):
        base = super(Settings, self).__dir__()
        return base + list(self.keys())

    def _reload(self):
        # type: () -> None

        if self._self_defaults:
            # we have to reload the `defaults` module otherwise
            # changed values (e.g. loaded from env var) won't show up
            try:
                module = import_module(self._self_defaults)
            except import_error_cls:
                # must have been a '{module.attr}' import path
                module = import_module(self._self_defaults.rsplit('.', 1)[0])
            reload_module(module)

        self._replace_wrapped(
            _load_config(self._self_initial_namespace, self._self_defaults)
        )

    def _replace_wrapped(self, new):
        # type: (ConfigLoader) -> None
        self.__wrapped__ = new


def _load_config(initial_namespace=None, defaults=None):
    # type: (Optional[str], Optional[str]) -> ConfigLoader
    """
    Kwargs:
        initial_namespace:
        defaults:
    """
    # load defaults
    if defaults:
        config = ConfigLoader()
        config.update_from_object(defaults)

    namespace = getattr(config, 'CONFIG_NAMESPACE', initial_namespace)
    app_config = getattr(config, 'APP_CONFIG', None)

    # load customised config
    if app_config:
        if namespace is None:
            config.update_from_object(app_config)
        else:
            _temp = ConfigLoader()
            _temp.update_from_object(app_config, lambda key: key.startswith(namespace))
            config.update(_temp.namespace(namespace))

    return config
