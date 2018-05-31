from flexisettings.utils import override_settings, override_environment

from test_lib.conf import settings
from test_lib.dummy import get_setting


def test_override_settings():
    """
    Does our `override_settings` util work?
    """
    assert get_setting('VAR1') == 'turkey'

    with override_settings(settings, VAR1='bacon'):
        assert get_setting('VAR1') == 'bacon'

    assert get_setting('VAR1') == 'turkey'


def test_override_environment():
    """
    Does our `override_environment` util work?
    """
    assert get_setting('VAR_FROM_ENV') == 'broccoli'

    with override_environment(settings, VAR_FROM_ENV='artichoke'):
        assert get_setting('VAR_FROM_ENV') == 'artichoke'

    assert get_setting('VAR_FROM_ENV') == 'broccoli'
