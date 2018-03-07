# -*- coding: utf-8 -*-
"""
.. module: mdc
.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

__version__ = '1.0.8'

import uuid
import logging
import datetime
import threading

from contextlib import contextmanager

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)

try:
    import ujson as json
except ImportError:
    LOGGER.debug('ujson not available, falling back to standard library')

    import json

logging._mdc = threading.local()


def merge_dicts(*dicts):
    result = {}

    for d in [ d for d in dicts if d]:
        result.update(**d)

    return result


@contextmanager
def MDC(**kwargs):
    context_id = str(uuid.uuid4())

    if hasattr(logging._mdc, context_id):
        context_id = str(uuid.uuid4())

    LOGGER.debug('creating context %s', context_id)

    setattr(logging._mdc, context_id, threading.local())

    context = getattr(logging._mdc, context_id)

    for key, value in kwargs.items():
        setattr(context, key, value)

    yield context

    LOGGER.debug('deleting context %s', context_id)

    try:
        delattr(logging._mdc, context_id)
    except AttributeError:
        LOGGER.warning('context was already deleted %s', context_id)


def with_mdc(**mdc_kwargs):
    def wrapped(f):
        def mdc_function(*args, **kwargs):
            with MDC(**mdc_kwargs) as context:
                return f(context, *args, **kwargs)
        return mdc_function
    return wrapped


class MDCFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, extra=None, **kwargs):
        super(MDCFormatter, self).__init__(fmt=fmt, datefmt=datefmt, **kwargs)

        self._extra = extra or []

    def format(self, record):
        try:
            message = record.getMessage()
        except Exception:
            message = str(record.msg)

        mdc_fields = merge_dicts(*list(vars(c) for c in vars(logging._mdc).values()))
        extra_fields = { f: getattr(record, f) for f in self._extra if hasattr(record, f) }

        exc_info = record.exc_info

        log_record = dict(
            message=message,
            logger=record.name,
            timestamp=datetime.datetime.utcfromtimestamp(record.created).isoformat(),
            level=record.levelname,
            mdc=mdc_fields,
            extra=extra_fields,
            python=dict(
                module=record.module,
                function=record.funcName,
                path=record.pathname,
                file=record.filename,
                line=record.lineno,
                process=dict(
                    name=record.processName,
                    id=record.process,
                ),
                thread=dict(
                    name=record.threadName,
                    id=record.thread,
                ),
            ),
        )

        if exc_info:
            log_record.update(
                exception=dict(
                    name=exc_info[0].__name__,
                    stacktrace=self.formatException(exc_info)
                )
            )

        return json.dumps(log_record)


class MDCHandler(logging.StreamHandler):
    def __init__(self, stream=None, extra=None, **kwargs):
        super(MDCHandler, self).__init__(stream)
        self.setFormatter(MDCFormatter(extra=extra, **kwargs))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
