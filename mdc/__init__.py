# -*- coding: utf-8 -*-
"""
.. module: mdc
.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import json
import logging
import threading

from contextlib import contextmanager


__version__ = '0.0.0'

logging._mdc = threading.local()


@contextmanager
def mdc(**kwargs):
    for key, value in kwargs.items():
        setattr(logging._mdc, key, value)

    yield

    for key in kwargs:
        delattr(logging._mdc, key)


def with_mdc(**mdc_kwargs):
    def wrapped(f):
        def mdc_function(*args, **kwargs):
            with mdc(**mdc_kwargs):
                return f(*args, **kwargs)
        return mdc_function
    return wrapped


class MDCFormatter(logging.Formatter):
    def format(self, record):
        record_vars = vars(record)
        record_vars.update(mdc=vars(logging._mdc))

        return json.dumps(record_vars)


class MDCHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        super(MDCHandler, self).__init__(*args, **kwargs)
        self.setFormatter(MDCFormatter())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
