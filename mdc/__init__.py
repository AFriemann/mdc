# -*- coding: utf-8 -*-
"""
.. module: mdc
.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library

standard_library.install_aliases()

import sys
import logging
import inspect
from functools import wraps

from mdc.context import *
from mdc.decorators import *

MDContext = new_log_context
MDC = new_log_context

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


def patch(old_factory):
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        for key, value in get_mdc_fields().items():
            setattr(record, key, value)
        return record

    return record_factory


try:
    logging.setLogRecordFactory(patch(logging.getLogRecordFactory()))
except AttributeError:
    logging.LogRecord = patch(logging.LogRecord)

