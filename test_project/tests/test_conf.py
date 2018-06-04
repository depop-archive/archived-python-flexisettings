from flexisettings.utils import override_settings, override_environment

from test_lib.conf import settings


def setup_function(function):
    settings._reload()


def teardown_function(function):
    settings._reload()


def test_defaults():
    """
    When constructing the Settings object we passed in a path to defaults,
    were (non-namespaced) values loaded from the defaults file?
    """
    assert settings.VAR1 == 'turkey'  # test_lib.conf.defaults.VAR1
    assert settings.VAR2 == 'sausage'  # test_lib.conf.defaults.VAR2


def test_override_settings():
    """
    Does our `override_settings` util work?
    """
    assert settings.VAR1 == 'turkey'

    with override_settings(settings, VAR1='bacon'):
        assert settings.VAR1 == 'bacon'

    assert settings.VAR1 == 'turkey'


def test_from_default_namespace():
    """
    If we set the APP_CONFIG env var, can we load (namespaced) values from the
    app config file into our test_lib settings?
    """
    with override_environment(settings, TEST_LIB_APP_CONFIG='app.settings'):
        assert settings.WHATEVER == 'WTF'  # app.settings.TEST_LIB_WHATEVER
        assert settings.VAR1 == 'chicken'  # app.settings.TEST_LIB_VAR1
        assert settings.VAR2 == 'sausage'  # test_lib.conf.defaults.VAR2


def test_from_custom_namespace():
    """
    If we set the CONFIG_NAMESPACE env var, can we load values from the
    app config file (using non-default namespace) into our test_lib settings?
    """
    with override_environment(
        settings,
        TEST_LIB_APP_CONFIG='app.settings',
        TEST_LIB_CONFIG_NAMESPACE='CUSTOM',
    ):
        assert not hasattr(settings, 'WHATEVER')
        assert settings.VAR1 == 'ostrich'  # app.settings.CUSTOM_VAR1
        assert settings.VAR2 == 'sausage'  # test_lib.conf.defaults.VAR2


def test_flexisettings_app_from_default_namespace():
    """
    (When the end-user app also uses flexisettings for its base config object)
    If we set the APP_CONFIG env var, can we load (namespaced) values from the
    app config file into our test_lib settings?
    """
    with override_environment(
        settings,
        TEST_LIB_APP_CONFIG='app2.conf.settings',
    ):
        assert settings.WHATEVER == 'WTF'  # app.settings.TEST_LIB_WHATEVER
        assert settings.VAR1 == 'chicken'  # app.settings.TEST_LIB_VAR1
        assert settings.VAR2 == 'sausage'  # test_lib.conf.defaults.VAR2


def test_flexisettings_app_from_custom_namespace():
    """
    (When the end-user app also uses flexisettings for its base config object)
    If we set the CONFIG_NAMESPACE env var, can we load values from the
    app config file (using non-default namespace) into our test_lib settings?
    """
    with override_environment(
        settings,
        TEST_LIB_APP_CONFIG='app2.conf.settings',
        TEST_LIB_CONFIG_NAMESPACE='CUSTOM',
    ):
        assert not hasattr(settings, 'WHATEVER')
        assert settings.VAR1 == 'ostrich'  # app.settings.CUSTOM_VAR1
        assert settings.VAR2 == 'sausage'  # test_lib.conf.defaults.VAR2
