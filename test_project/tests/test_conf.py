import pytest

from flexisettings import Settings
from flexisettings.utils import override_settings

from .utils import override_environment


@pytest.fixture
def settings():
    return Settings('TEST_LIB', 'test_lib.conf.defaults')


def test_defaults(settings):
    """
    When constructing the Settings object we passed in a path to defaults,
    were (non-namespaced) values loaded from the defaults file?
    """
    assert settings.VAR1 == 'turkey'  # test_lib.conf.defaults.VAR1
    assert settings.VAR2 == 'sausage'  # test_lib.conf.defaults.VAR2


def test_override_settings(settings):
    """
    Does our `override_settings` util work?
    """
    assert settings.VAR1 == 'turkey'

    with override_settings(settings, VAR1='bacon'):
        assert settings.VAR1 == 'bacon'

    assert settings.VAR1 == 'turkey'


def test_from_default_namespace(settings):
    """
    If we set the APP_CONFIG env var, can we load (namespaced) values from the
    app config file into our test_lib settings?
    """
    with override_environment(TEST_LIB_APP_CONFIG='app.settings'):
        settings._reload()
        assert settings.WHATEVER == 'WTF'  # app.settings.TEST_LIB_WHATEVER
        assert settings.VAR1 == 'chicken'  # app.settings.TEST_LIB_VAR1
        assert settings.VAR2 == 'sausage'  # test_lib.conf.defaults.VAR2


def test_from_custom_namespace(settings):
    """
    If we set the CONFIG_NAMESPACE env var, can we load values from the
    app config file (using non-default namespace) into our test_lib settings?
    """
    with override_environment(
        TEST_LIB_APP_CONFIG='app.settings',
        TEST_LIB_CONFIG_NAMESPACE='CUSTOM'
    ):
        settings._reload()
        assert not hasattr(settings, 'WHATEVER')
        assert settings.VAR1 == 'ostrich'  # app.settings.CUSTOM_VAR1
        assert settings.VAR2 == 'sausage'  # test_lib.conf.defaults.VAR2
