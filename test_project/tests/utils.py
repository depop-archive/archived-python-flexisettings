import os
from contextlib import contextmanager


@contextmanager
def override_environment(**kwargs):
    old_env = os.environ
    new_env = os.environ.copy()
    new_env.update(kwargs)
    os.environ = new_env
    yield
    os.environ = old_env
