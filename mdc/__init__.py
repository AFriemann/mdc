# -*- coding: utf-8 -*-
"""
.. module: mdc
.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

__version__ = '1.1.0'

import logging

from mdc.formatter import MDCFormatter, JSONMDCFormatter
from mdc.context import MDContext

MDC = MDContext

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


def merge_dicts(*dicts):
    result = {}

    for d in [ d for d in dicts if d]:
        result.update(**d)

    return result


def with_mdc(**mdc_kwargs):
    def wrapped(f):
        def mdc_function(*args, **kwargs):
            with MDC(**mdc_kwargs) as context:
                return f(context, *args, **kwargs)
        return mdc_function
    return wrapped


class MDCHandler(logging.StreamHandler):
    def __init__(self, stream=None, extra=None, json=True, fmt=None, **kwargs):
        super(MDCHandler, self).__init__(stream)

        if json:
            formatter = JSONMDCFormatter(extra=extra, **kwargs)
        else:
            formatter = MDCFormatter(extra=extra, fmt=fmt, **kwargs)

        self.setFormatter(formatter)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
