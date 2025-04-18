from time import time

from paul_tools.Decorator.retry import retry

from .__init__ import pytest


def test_retry_success():
    """
    Test the retry decorator to ensure it retries the function until it succeeds.
    This test defines a function `succeed_after_two_attempts` that will fail twice
    before succeeding on the third attempt. The `retry` decorator is applied to this
    function with a delay of 0.1 seconds between retries. The test verifies that the
    function eventually returns "Success" and that the number of attempts is exactly 3.
    """
    attempts = 0

    @retry(delay=0.1)
    def succeed_after_two_attempts():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Fail")
        return "Success"

    assert succeed_after_two_attempts() == "Success"
    assert attempts == 3


def test_retry_failure():
    """
    Test the retry decorator to ensure it retries the specified number of times on failure.
    This test defines a function `always_fail` that always raises a `ValueError`.
    The `retry` decorator is applied to this function with 3 retries and a delay of 0.1 seconds between retries.
    The test verifies that the `always_fail` function is called exactly 3 times and that it raises a `ValueError` with the message "Fail".
    Assertions:
    - The `always_fail` function raises a `ValueError` with the message "Fail".
    - The `always_fail` function is called exactly 3 times.
    """
    attempts = 0

    @retry(retries=3, delay=0.1)
    def always_fail():
        nonlocal attempts
        attempts += 1
        raise ValueError("Fail")

    with pytest.raises(ValueError, match="Fail"):
        always_fail()
    assert attempts == 3


def test_retry_invalid_parameters():
    """
    Test the retry decorator with invalid parameters.
    This test checks that the retry decorator raises a ValueError when given
    invalid parameters. Specifically, it verifies that:
    - A ValueError is raised when the number of retries is less than 1.
    - A ValueError is raised when the delay is less than or equal to 0.
    The error message is expected to match the regular expression:
        r"(retries not < 1 or delay not <= 0|重試次數不 < 1 或延遲不 <= 0)"
    """
    import re

    reg = re.compile(
        r"(retries not < 1 or delay not <= 0|重試次數不 < 1 或延遲不 <= 0)"
    )
    with pytest.raises(ValueError, match=reg):

        @retry(retries=0, delay=0.1)
        def invalid_retries():  # pragma: no cover
            pass

    with pytest.raises(ValueError, match=reg):

        @retry(retries=3, delay=0)
        def invalid_delay():  # pragma: no cover
            pass


def test_retry_delay():
    """
    Test the retry decorator with a delay between retries.
    This test verifies that the `retry` decorator correctly retries a function
    that raises an exception, with a specified delay between each retry.
    The test function `fail_with_delay` is decorated with `@retry(retries=3, delay=0.5)`,
    which means it should be retried 3 times with a 0.5-second delay between each attempt.
    The function raises a `ValueError` on each attempt.
    The test checks the following:
    1. The function is retried the correct number of times (3 attempts).
    2. The total time taken for the retries includes the specified delays (at least 1.0 seconds).
    Assertions:
    - `attempts` should be equal to 3 after the retries.
    - The difference between `end_time` and `start_time` should be at least 1.0 seconds,
        accounting for the 2 delays of 0.5 seconds each.
    """
    attempts = 0

    @retry(retries=3, delay=0.5)
    def fail_with_delay():
        nonlocal attempts
        attempts += 1
        raise ValueError("Fail")

    start_time = time()
    with pytest.raises(ValueError, match="Fail"):
        fail_with_delay()
    end_time = time()

    assert attempts == 3
    assert end_time - start_time >= 1.0  # 2 delays of 0.5 seconds each
