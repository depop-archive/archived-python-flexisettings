flexisettings
=============

|Build Status|

.. |Build Status| image:: https://circleci.com/gh/depop/python-flexisettings.svg?style=shield&circle-token=ae7b355ec3b18c69d3370898a69932091c43d152
    :alt: Build Status

Partly inspired by Django's ``from django.conf import settings`` settings object.

The goal is to allow shared libraries to be configured by a settings file in
the project which imports them (like how Django libraries can expect the Django
``settings`` object to exist).

Usage
-----

We want the shared lib to be able to load config values *from the app which is*
*importing it*.

A suggested layout would be as found in ``test_project/test_lib`` in this repo.
For example, create a ``test_lib/conf/__init__.py`` like:

.. code:: python

	from flexisettings import Settings

	settings = Settings(initial_namespace='TEST_LIB', defaults='test_lib.conf.defaults')

We have a concept of customisable 'namespace' (prefix) for config values. This
is as defined by the `ConfigLoader <https://pypi.python.org/pypi/configloader>`_
lib we are making use of.

``initial_namespace`` is the default namespace for config values of your shared
lib. Projects who want to use your lib will be able to customise the namespace,
but as they are used for bootstrapping there are two config values which will
*always* use the default name (``APP_CONFIG`` and ``CONFIG_NAMESPACE``).

So for example, say ``myapp`` wants to use ``test_lib``. ``myapp`` can
customise the namespace by defining ``TEST_LIB_CONFIG_NAMESPACE = 'CUSTOM'``.

``defaults`` is the import path to a python module or object *in your shared lib*
which contains default values for your config. These keys should *not* be
namespaced.

For example if you want the config namespace for your shared lib to be
configurable via env var you could create ``test_lib/conf/defaults.py`` like:

.. code:: python

	import os

	# namespace for config keys loaded from e.g. Django conf or env vars
	CONFIG_NAMESPACE = os.getenv('TEST_LIB_CONFIG_NAMESPACE', 'TEST_LIB')

	APP_CONFIG = os.getenv('TEST_LIB_APP_CONFIG', None)

Then ``myapp`` would be able to ``export TEST_LIB_CONFIG_NAMESPACE=CUSTOM``.

That explains namespace customisation a bit, what about the ``APP_CONFIG``?

Say for example that ``myapp`` is a Django website and ``test_lib`` has the
defaults file shown above. In your ``myapp`` project you could:

.. code:: bash

	export TEST_LIB_CONFIG_NAMESPACE=CUSTOM
	export TEST_LIB_APP_CONFIG=django.conf.settings

Then in ``myapp/settings.py`` you could have:

.. code:: python

	CUSTOM_VAR1 = 'whatever'

Now, recall the ``test_lib/conf/__init__.py`` that we created at the start. In
your ``test_lib`` code you could have:

.. code:: python

	from test_lib.conf import settings

	assert settings.VAR1 == 'whatever'

As you can see the ``VAR1`` was set in the importing project's Django settings
with the ``CUSTOM_`` prefix but is available in your shared lib's ``settings``
object under its non-prefixed name.

Compatibility
-------------

This project is tested against:

=========== ===
Python 2.7   * 
Python 3.6   * 
=========== ===

Running the tests
-----------------

CircleCI
~~~~~~~~

| The easiest way to test the full version matrix is to install the
  CircleCI command line app:
| https://circleci.com/docs/2.0/local-jobs/
| (requires Docker)

The cli does not support 'workflows' at the moment so you have to run
the two Python version jobs separately:

.. code:: bash

    circleci build --job python-2.7

.. code:: bash

    circleci build --job python-3.6

py.test (single python version)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's also possible to run the tests locally, allowing for debugging of
errors that occur.

Now decide which Python version you want to test and create a virtualenv:

.. code:: bash

    pyenv virtualenv 3.6.4 flexisettings
    pip install -r requirements-test.txt

The code in ``test_project`` demonstrates collaborative config between a shared
library ``test_lib`` and the app that wants to use it ``app``. Set the path to
the test project

.. code:: bash

    make test
