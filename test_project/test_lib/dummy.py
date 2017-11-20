from test_lib.conf import settings


def get_setting(name):
    return getattr(settings, name)
