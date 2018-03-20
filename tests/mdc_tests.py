# -*- coding: utf-8 -*-

import logging

from mdc import with_mdc, with_thread_mdc, MDC, MDCHandler, Formatter

hndlr = MDCHandler(extra=['foo'])
logging.root.addHandler(hndlr)


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
        logging.exception(e, extra=dict(foo='oink'))


def test_mdc_decorator():
    @with_mdc(baz='bar')
    def foobar(ctx, x):
        logging.debug(x)

        assert ctx.baz == 'bar', ctx.baz

    foobar(1)

def test_thread_mdc():
    formatter = Formatter('[%(foo)s/%(bar)s/%(blah)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    hndlr.setFormatter(formatter)
    @with_thread_mdc(bar='def')
    def bar(ctx, x):
        logging.debug(x)
        assert ctx.bar == 'def', ctx.bar
        assert ctx.foo == 'abc', ctx.foo

    @with_thread_mdc(foo='abc')
    def foo(ctx, x):
        logging.debug(x)
        assert ctx.foo == 'abc', ctx.foo
        bar(1)
        assert ctx.foo == 'abc', ctx.foo
        assert hasattr(ctx, 'bar') == False, vars(ctx)
    foo(1)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
