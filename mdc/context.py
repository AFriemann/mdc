# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import uuid
import logging
import threading

from contextlib import contextmanager

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)

logging._mdc = threading.local()


@contextmanager
def MDContext(**kwargs):
    context_id = 'mdc-{thread}-{context}'.format(
        thread=threading.current_thread().ident,
        context=uuid.uuid4())

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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
