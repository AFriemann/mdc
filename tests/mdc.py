# -*- coding: utf-8 -*-

import logging

from mdc import mdc, with_mdc


def test_attaching_fields():
    assert logging._mdc is not None

    with mdc(foo='bar'):
        assert logging._mdc is not None
        assert logging._mdc.foo == 'bar'

        logging.debug('abc', extra={'foo': 'bar'})

    assert not hasattr(logging._mdc, 'foo')


def test_mdc_decorator():
    @with_mdc(baz='bar')
    def foobar(x):
        logging.debug(x)

        assert logging._mdc.baz == 'bar', logging._mdc.baz

    foobar(1)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
