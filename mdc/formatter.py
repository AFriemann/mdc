# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import logging
import datetime
import warnings
import collections


try:
    import ujson as json
except ImportError:
    warnings.warn('ujson not available, falling back to standard json library')

    import json


class MDCFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, extra=None, **kwargs):
        super(MDCFormatter, self).__init__(fmt=fmt, datefmt=datefmt, **kwargs)

        self._extra = extra or dict()

    def get_mdc_fields(self):
        result = collections.defaultdict(None)

        for c in (vars(ctx) for ctx in vars(logging._mdc).values()):
            result.update(**c)

        return result

    def get_extra_fields(self, record):
        return {
            f: getattr(record, f)
            for f in self._extra if hasattr(record, f)}

    def format(self, record):
        mdc_fields = self.get_mdc_fields()
        extra_fields = self.get_extra_fields(record)

        for k, v in (list(extra_fields.items()) + list(mdc_fields.items())):
            setattr(record, k, v)

        try:
            return super(MDCFormatter, self).format(record)
        except KeyError as e:
            setattr(record, '%s' % e.args[0], None)
            return self.format(record)


class JSONMDCFormatter(MDCFormatter):
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
            mdc=self.get_mdc_fields(),
            extra=self.get_extra_fields(record),
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

        if record.exc_info:
            log_record.update(
                exception=dict(
                    name=record.exc_info[0].__name__,
                    stacktrace=self.formatException(record.exc_info)
                )
            )

        return json.dumps(log_record)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
