from io import StringIO

from paul_tools.Decorator.debug import debug

from .__init__ import pytest


def test_debug_logs_correct_messages():
    """
    Test the debug decorator to ensure it logs the correct messages.
    This test defines a sample function decorated with the `debug` decorator,
    which logs messages before and after the function execution. The log
    messages are captured using a `StringIO` stream.
    The test verifies that:
    - The log contains a message indicating the function execution started.
    - The log contains a message indicating the function execution ended.
    - The log contains the result of the function execution.
    - The function returns the correct result.
    Assertions:
        - "sample_function#before" is in the log contents.
        - "sample_function#after" is in the log contents.
        - "result: 5" is in the log contents.
        - The result of `sample_function(2, 3)` is 5.
    """

    @debug(logFn=lambda x: print(x, file=log_stream))
    def sample_function(x: int | float, y: int | float) -> int | float:
        return x + y

    log_stream = StringIO()

    result = sample_function(2, 3)

    log_contents = log_stream.getvalue()

    assert "sample_function#before" in log_contents
    assert "sample_function#after" in log_contents
    assert "result: 5" in log_contents
    assert result == 5


def test_debug_return_value():
    """
    Test the `debug` decorator to ensure it correctly logs and returns the expected value.
    This test defines a function `return_value` decorated with `debug()`. The function
    returns a string "Expected Value". The test then calls the decorated function and
    asserts that the returned value matches the expected string.
    The `debug` decorator is assumed to log the function call details, but this test
    focuses on verifying the return value.
    Assertions:
        - The result of calling `return_value()` should be "Expected Value".
    """

    @debug()
    def return_value():
        return "Expected Value"

    result = return_value()
    assert result == "Expected Value"


def test_debug_exception_handling():
    """
    Test the debug decorator's exception handling.
    This test verifies that the debug decorator correctly handles exceptions
    raised within the decorated function. It uses the `pytest.raises` context
    manager to assert that a ValueError with the message "This is an error" is
    raised when the `raise_exception` function is called.
    The `raise_exception` function is decorated with the `debug` decorator,
    which is expected to log the function call and its exception.
    Assertions:
        - A ValueError with the message "This is an error" is raised when
          `raise_exception` is called.
    """

    @debug()
    def raise_exception():
        raise ValueError("This is an error")

    with pytest.raises(ValueError, match="This is an error"):
        raise_exception()
