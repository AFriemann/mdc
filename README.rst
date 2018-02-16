MDC
===

Installation
------------

PyPi:

.. code:: bash

  $ pip install --user mdc

From source:

.. code:: bash

  $ pip install --user .

Usage
-----

.. code:: python

  >>> import logging
  >>> from mdc import MDCHandler, mdc

  >>> logging.root.addHandler(MDCHandler())

  >>> logging.warning('foobar')
  {"name": "root", "msg": "warning foobar", "args": [], "levelname": "WARNING", "levelno": 30, "pathname": "...", "filename": "...", "module": "test", "exc_info": null, "exc_text": null, "stack_info": null, "lineno": ..., "funcName": "...", "created": ..., "msecs": ..., "relativeCreated": ..., "thread": ..., "threadName": "MainThread", "processName": "MainProcess", "process": ..., "mdc": {}}

  >>> with mdc(foo='bar'):
  ...     logging.warning('foobar')
  {"name": "root", "msg": "warning foobar", "args": [], "levelname": "WARNING", "levelno": 30, "pathname": "...", "filename": "...", "module": "test", "exc_info": null, "exc_text": null, "stack_info": null, "lineno": ..., "funcName": "...", "created": ..., "msecs": ..., "relativeCreated": ..., "thread": ..., "threadName": "MainThread", "processName": "MainProcess", "process": ..., "mdc": {"foo": "bar"}}

  >>> logging.warning('foobar')
  {"name": "root", "msg": "warning foobar", "args": [], "levelname": "WARNING", "levelno": 30, "pathname": "...", "filename": "...", "module": "test", "exc_info": null, "exc_text": null, "stack_info": null, "lineno": ..., "funcName": "...", "created": ..., "msecs": ..., "relativeCreated": ..., "thread": ..., "threadName": "MainThread", "processName": "MainProcess", "process": ..., "mdc": {}}


Running tests:

.. code:: bash

  $ tox
