# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import contextvars

from future import standard_library

standard_library.install_aliases()
import time
import uuid
import logging
import collections

from contextlib import contextmanager

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)

CREATION_TIME_KEY = "__creation_time__"

logging._mdc = contextvars.ContextVar('mdc', default={})
start = time.time()


def get_mdc_fields():
    result = collections.defaultdict(None)
    contexts = logging._mdc.get()
    for context_id, values in sorted(contexts.items(), key=lambda kv: kv[1][CREATION_TIME_KEY]):
        actual_context = {k: values[k] for k in values if k != CREATION_TIME_KEY}
        result.update(**actual_context)
    return result


@contextmanager
def new_log_context(**kwargs):
    context_id = str(uuid.uuid4())

    LOGGER.debug("creating context %s", context_id)

    context = logging._mdc.get()
    current_context = {}
    current_context[CREATION_TIME_KEY] = time.time() - start

    for key, value in kwargs.items():
        current_context[key] = value

    context[context_id] = current_context
    logging._mdc.set(context)

    try:
        print(current_context)
        yield current_context
    finally:
        LOGGER.debug("deleting context %s", context_id)

        try:
            context = logging._mdc.get()
            del context[context_id]
        except AttributeError:
            LOGGER.warning("context was already deleted %s", context_id)


MDContext = new_log_context
