import logging

from mdc import with_mdc, MDC, log_value, new_log_context, log_argument


def assert_context_has(**kwargs):
    record = logging.makeLogRecord({})
    for key, value in kwargs.items():
        assert hasattr(record, key)
        assert getattr(record, key) == value


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


def test_generator():
    @log_value(inside=True)
    def my_generator():
        for i in range(5):
            record = logging.makeLogRecord({})

            assert hasattr(record, "inside")
            assert record.inside == True

            yield i

    with new_log_context(inside=False) as ctx:
        for _ in my_generator():
            assert ctx.inside == False


def test_log_value():
    @log_value(foo="bar")
    def my_function():
        assert_context_has(foo="bar")

    assert not hasattr(logging.makeLogRecord({}), "foo")
    my_function()
    assert not hasattr(logging.makeLogRecord({}), "foo")


def test_nested_contexts():

    with new_log_context(food="spam"):
        with new_log_context(food="ham"):
            with new_log_context(food="eggs"):
                assert_context_has(food="eggs")
            assert_context_has(food="ham")
        assert_context_has(food="spam")


def test_log_argument():
    @log_argument("food")
    def eat(food):
        assert_context_has(food=food)

    for food in ["spam", "ham", "eggs"]:
        eat(food)


def test_log_argument_with_destination():
    @log_argument("food", "abcd")
    def eat(food):
        assert_context_has(abcd=food)

    for food in ["spam", "ham", "eggs"]:
        eat(food)


def test_log_argument_with_formatter():
    @log_argument("food", formatter=str.upper)
    def eat(food):
        assert_context_has(food=str.upper(food))

    for food in ["spam", "ham", "eggs"]:
        eat(food)
