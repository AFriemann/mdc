MDC
===

.. image:: https://travis-ci.org/AFriemann/mdc.svg?branch=master
    :target: https://travis-ci.org/AFriemann/mdc

This is thought to be an easy to use, import and go, library for Mapped Diagnostic Context style logging.

Logs should include all necessary fields collected by the python logging library.
Helper methods are provided to add context fields where required.

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

Add a handler to the root logger or set the base handler with *logging.basicConfig*:

.. code:: python

  >>> import logging
  >>> from mdc import MDCHandler

  >>> # use the MDCHandler only
  >>> logging.basicConfig(level=logging.DEBUG, handlers=[MDCHandler()])

  >>> # the MDC contextmanager
  >>> with MDC(foo='bar'):
  ...     logging.warning('foobar')
  { ..., "mdc": { "foo": "bar" }, "extra": {}, ... }

  >>> # the with_mdc decorator
  >>> @with_mdc(test='123')
  ... def foobar(ctx):
  ...   logging.warning('some warning')

  >>> foobar()
  { ..., "mdc": { "test": "123" }, "extra": {}, ... }

  >>> # logging with extra fields
  >>> logging.error('some error', extra=dict(foo='bar'))
  { ..., "mdc": {}, "extra": { "foo": "bar" }, ... }

By default log messages will include the following fields:

.. code:: json

  {
    "message": "deleting context b8321b4f-19ff-4c98-b011-5a97178e7ad6",
    "logger": "mdc",
    "timestamp": "2018-03-07T21:39:12.010851",
    "level": "DEBUG",
    "mdc": {
      "foo": "bar",
      "index": 76
    },
    "extra": {},
    "python": {
      "module": "__init__",
      "function": "MDC",
      "path": "/home/user/git/mdc/mdc/__init__.py",
      "file": "__init__.py",
      "line": 56,
      "process": {
        "name": "MainProcess",
        "id": 31678
      },
      "thread": {
        "name": "MainThread",
        "id": 140433289192768
      }
    }
  }

Running tests:

.. code:: bash

  $ tox

