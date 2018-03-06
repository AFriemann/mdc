# -*- coding: utf-8 -*-
"""
.. module: mdc
.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

__version__ = '1.0.5'

import json
import logging
import datetime
import threading

from contextlib import contextmanager

logging._mdc = threading.local()


@contextmanager
def MDC(**kwargs):
    for key, value in kwargs.items():
        setattr(logging._mdc, key, value)

    yield

    for key in kwargs:
        try:
            delattr(logging._mdc, key)
        except AttributeError:
            pass


def with_mdc(**mdc_kwargs):
    def wrapped(f):
        def mdc_function(*args, **kwargs):
            with MDC(**mdc_kwargs):
                return f(*args, **kwargs)
        return mdc_function
    return wrapped


class MDCFormatter(logging.Formatter):
    def format(self, record):
        try:
            message = record.getMessage()
        except Exception:
            message = str(record.msg)

        log_record = dict(
            message=message,
            logger=record.name,
            timestamp=datetime.datetime.utcfromtimestamp(record.created).isoformat(),
            level=record.levelname,
            mdc=vars(logging._mdc),
            python=dict(
                module=record.module,
                function=record.funcName,
                path=record.pathname,
                line=record.lineno,
                process=dict(
                    name=record.processName,
                    pid=record.process,
                ),
                thread=dict(
                    name=record.threadName,
                    tid=record.thread,
                ),
            ),
        )

        if record.exc_info:
            log_record.update(
                exception=dict(
                    name=record.exc_info[0].__name__,
                    stacktrace=self.formatException(record.exc_info)
                )
            )

        return json.dumps(log_record)


class MDCHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        super(MDCHandler, self).__init__(*args, **kwargs)
        self.setFormatter(MDCFormatter())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
