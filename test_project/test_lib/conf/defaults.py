import os


# namespace for config keys loaded from e.g. Django conf or env vars
CONFIG_NAMESPACE = os.getenv('TEST_LIB_CONFIG_NAMESPACE', 'TEST_LIB')

# optional import path to file containing namespaced config (e.g. 'django.conf.settings')
APP_CONFIG = os.getenv('TEST_LIB_APP_CONFIG', None)


VAR1 = 'turkey'

VAR2 = 'sausage'
