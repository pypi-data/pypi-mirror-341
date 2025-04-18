import sys
from io import StringIO
from time import sleep

from paul_tools.Decorator.getTime import getTime

from .__init__ import pytest


def test_getTime_prints_execution_time():
    """
    Test the getTime decorator to ensure it prints the execution time of the decorated function.
    This test defines a sample function decorated with getTime, captures the printed output,
    and verifies that the output contains the function name and the execution time message.
    It also checks that the sample function returns the expected result.
    Assertions:
    - The output contains the name of the sample function.
    - The output contains the execution time message in English or Chinese.
    - The sample function returns "Done".
    """
    from paul_tools.Decorator.getTime import logger

    @getTime
    def sample_function():
        sleep(0.1)
        return "Done"

    captured_output = StringIO()
    sys.stdout = captured_output
    logger.add(captured_output, format="{message}")
    result = sample_function()
    logger.remove()
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "sample_function" in output
    assert "Execution time is" in output or "執行時間為" in output
    assert result == "Done"


def test_getTime_return_value():
    """
    Test the getTime decorator to ensure it does not alter the return value of the decorated function.
    This test defines a function `return_value` that returns a string "Expected Value" and decorates it with `getTime`.
    It then calls the decorated function and asserts that the return value is still "Expected Value".
    """

    @getTime
    def return_value():
        return "Expected Value"

    result = return_value()
    assert result == "Expected Value"


def test_getTime_exception_handling():
    """
    Test the getTime decorator to ensure it correctly handles exceptions.
    This test defines a function `raise_exception` that raises a ValueError.
    The function is decorated with `getTime`. The test then verifies that
    calling `raise_exception` raises a ValueError with the expected message.
    The test uses pytest's `raises` context manager to check for the exception.
    Raises:
        ValueError: If the exception is not raised or the message does not match.
    """

    @getTime
    def raise_exception():
        raise ValueError("This is an error")

    with pytest.raises(ValueError, match="This is an error"):
        raise_exception()
