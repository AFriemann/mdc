# -*- coding: utf-8 -*-

import logging

from mdc import with_mdc, MDC, MDCHandler

logging.root.addHandler(MDCHandler())


def test_attaching_fields():
    assert logging._mdc is not None

    with MDC(foo='bar') as context:
        assert context is not None
        assert context.foo == 'bar'

        logging.debug('abc')

        with MDC(bar='foo') as context2:
            assert context2 is not None
            assert context2.bar == 'foo'

    try:
        raise RuntimeError('test')
    except Exception as e:
        logging.exception(e)


def test_mdc_decorator():
    @with_mdc(baz='bar')
    def foobar(ctx, x):
        logging.debug(x)

        assert ctx.baz == 'bar', ctx.baz

    foobar(1)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
