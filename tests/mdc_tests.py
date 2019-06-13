import logging

from mdc import with_mdc, MDC


def test_attaching_fields():
    assert logging._mdc is not None

    with MDC(foo="bar") as context:
        assert context is not None
        assert context.foo == "bar"

        logging.debug("abc")

        with MDC(bar="foo") as context2:
            assert context2 is not None
            assert context2.bar == "foo"

    try:
        raise RuntimeError("test")
    except Exception as e:
        logging.exception(e, extra=dict(foo="oink"))


def test_mdc_decorator():
    @with_mdc(baz="bar")
    def foobar(x, ctx=None):
        logging.debug(x)

        assert ctx.baz == "bar", ctx.baz

    foobar(1)
