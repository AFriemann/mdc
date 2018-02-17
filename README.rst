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

  >>> logging.basicConfig(level=logging.DEBUG, handlers=[MDCHandler()])

By default log messages will include the following fields:

.. code:: json


  {
    "message": "...",
    "logger": "...",
    "timestamp": "2018-02-17T16:39:53.475377",
    "level": "DEBUG",
    "mdc": {},
    "python": {
      "module": "...",
      "function": "...",
      "path": "...",
      "line": 0,
      "process": {
        "name": "MainProcess",
        "pid": 3724
      },
      "thread": {
        "name": "MainThread",
        "tid": 140050978850112
      }
    }
  }

You can use the provided decorator or contextmanager to add MDC fields:

.. code:: python

  >>> from mdc import MDC, with_mdc

  >>> with MDC(foo='bar'):
  ...     logging.warning('foobar')

  >>> @with_mdc(test='123')
  ... def foobar():
  ...   pass

Running tests:

.. code:: bash

  $ tox

