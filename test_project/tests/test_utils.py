from flexisettings.utils import override_settings

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
