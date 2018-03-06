# -*- coding: utf-8 -*-
"""
.. module: mdc
.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

__version__ = '1.0.7'

import json
import uuid
import logging
import datetime
import threading

from contextlib import contextmanager


logging._mdc = threading.local()

LOGGER = logging.getLogger(__name__)


def merge_dicts(*dicts):
    result = {}

    for d in [ d for d in dicts if d]:
        result.update(**d)

    return result


@contextmanager
def MDC(**kwargs):
    context_id = uuid.uuid4().hex

    if not hasattr(logging._mdc, context_id):
        LOGGER.debug('creating context %s', context_id)

        setattr(logging._mdc, context_id, threading.local())

    context = getattr(logging._mdc, context_id)

    for key, value in kwargs.items():
        setattr(context, key, value)

    yield context

    for key in kwargs:
        LOGGER.debug('deleting context %s', context_id)

        try:
            delattr(logging._mdc, context_id)
        except AttributeError:
            pass


def with_mdc(**mdc_kwargs):
    def wrapped(f):
        def mdc_function(*args, **kwargs):
            with MDC(**mdc_kwargs) as context:
                return f(context, *args, **kwargs)
        return mdc_function
    return wrapped


class MDCFormatter(logging.Formatter):
    def format(self, record):
        try:
            message = record.getMessage()
        except Exception:
            message = str(record.msg)

        fields = list(vars(c) for c in vars(logging._mdc).values())

        log_record = dict(
            message=message,
            logger=record.name,
            timestamp=datetime.datetime.utcfromtimestamp(record.created).isoformat(),
            level=record.levelname,
            mdc=merge_dicts(*fields),
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
