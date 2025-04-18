import sys
from io import StringIO

from paul_tools.Decorator.noPrint import noPrint

from .__init__ import pytest


def test_noPrint_no_output():
    """
    Test the noPrint decorator to ensure that it suppresses output.
    This test defines a function `print_something` that prints a message.
    The function is decorated with `@noPrint` to suppress its output.
    The test captures the standard output and verifies that nothing is printed.
    Asserts:
        The captured output is an empty string, indicating no output was printed.
    """

    @noPrint
    def print_something():
        print("This should not be printed")

    captured_output = StringIO()
    sys.stdout = captured_output
    print_something()
    sys.stdout = sys.__stdout__

    assert captured_output.getvalue() == ""


def test_noPrint_return_value():
    """
    Test the noPrint decorator to ensure it does not affect the return value of the decorated function.
    This test defines a function `return_value` that returns a string "Expected Value" and decorates it with `@noPrint`.
    It then calls the decorated function and asserts that the return value is still "Expected Value".
    The purpose of this test is to verify that the `noPrint` decorator does not alter the return value of the function it decorates.
    """

    @noPrint
    def return_value():
        return "Expected Value"

    result = return_value()
    assert result == "Expected Value"


def test_noPrint_exception_handling():
    """
    Test the `noPrint` decorator to ensure it correctly handles exceptions.
    This test defines a function `raise_exception` decorated with `noPrint`
    that raises a `ValueError`. It then uses `pytest.raises` to assert that
    the `ValueError` is raised with the expected error message.
    The `noPrint` decorator is expected to suppress any print statements
    within the decorated function, but it should not interfere with the
    exception being raised and propagated.
    """

    @noPrint
    def raise_exception():
        raise ValueError("This is an error")

    with pytest.raises(ValueError, match="This is an error"):
        raise_exception()
