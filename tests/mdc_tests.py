# -*- coding: utf-8 -*-

import logging

from mdc import with_mdc, MDC, MDCHandler

logging.root.addHandler(MDCHandler())


def test_attaching_fields():
    assert logging._mdc is not None

    with MDC(foo='bar'):
        assert logging._mdc is not None
        assert logging._mdc.foo == 'bar'

        logging.debug('abc')

    assert not hasattr(logging._mdc, 'foo')

    try:
        raise RuntimeError('test')
    except Exception as e:
        logging.exception(e)


def test_mdc_decorator():
    @with_mdc(baz='bar')
    def foobar(x):
        logging.debug(x)

        assert logging._mdc.baz == 'bar', logging._mdc.baz

    foobar(1)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
