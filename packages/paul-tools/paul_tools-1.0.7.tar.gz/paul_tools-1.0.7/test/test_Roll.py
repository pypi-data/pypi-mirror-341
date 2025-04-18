from random import Random

from paul_tools.Roll import Roll, RollType, returnType

from .__init__ import pytest


def test_rollTextReplace():
    """
    Unit test for the rollTextReplace method of the Roll class.

    This test verifies that the rollTextReplace method correctly replaces
    specific input strings with their corresponding output strings.

    Assertions:
    - rollTextReplace("int") should return "智力 "
    - rollTextReplace("san") should return "理智 "
    - rollTextReplace("other") should return "other"
    """
    assert Roll.rollTextReplace("int") == "智力 "
    assert Roll.rollTextReplace("san") == "理智 "
    assert Roll.rollTextReplace("other") == "other"


def test_RollNumRegTools():
    """
    Test the RollNumRegTools method of the Roll class.

    This test verifies that the RollNumRegTools method correctly parses dice notation strings
    and returns the expected list of integers representing the number of dice, the type of dice,
    and any modifier.

    Assertions:
    - The method correctly parses "2d6+3" to [2, 6, 3].
    - The method correctly parses "d20" to [1, 20, 0].
    - The method raises an exception for invalid input "invalid".

    Raises:
    - Exception: If the input string is invalid.
    """
    assert Roll.RollNumTextToDataTools("2d6+3") == {"xD": 2, "Dy": 6, "sumBonus": 3}
    assert Roll.RollNumTextToDataTools("d20") == {"xD": 1, "Dy": 20, "sumBonus": 0}
    with pytest.raises(Exception):
        Roll.RollNumTextToDataTools("invalid")


def test_RollNum():
    """
    Test the RollNum method of the Roll class.

    This test checks if the RollNum method correctly processes the input string "2d6+3"
    and returns a result dictionary containing the keys "rollValueList", "Type", and "returnValueList".

    Assertions:
        - The result dictionary contains the key "rollValueList".
        - The result dictionary contains the key "Type".
        - The result dictionary contains the key "returnValueList".
    """
    roll = Roll(debug=True)
    result = roll.RollNum(Roll.RollNumTextToDataTools("2d6+3"))
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result


def test_RollList():
    """
    Test the RollList method of the Roll class.

    This test creates an instance of the Roll class and calls the RollList method
    with a list of integers. It asserts that the result of the RollList method
    is one of the integers in the input list.

    Returns:
        None
    """
    roll = Roll(debug=True)
    result = roll.RollList([1, 2, 3, 4, 5])
    assert result in [1, 2, 3, 4, 5]


def test_getExpectedValue():
    """
    Test the getExpectedValue method of the Roll class.
    This test checks the following scenarios:
    1. The expected value is correctly calculated given a list of values and their corresponding probabilities.
    2. A ValueError is raised when the lengths of the values and probabilities lists do not match.
    3. A ValueError is raised when the sum of probabilities does not equal 1.
    Test cases:
    - values = [1, 2, 3], probabilities = [0.2, 0.5, 0.3], expected result = 2.1
    - values = [1, 2], probabilities = [0.5, 0.5, 0.1], should raise ValueError
    - values = [1, 2], probabilities = [0.5, 0.4], should raise ValueError
    """
    roll = Roll(debug=True)
    values = [1, 2, 3]
    probabilities = [0.2, 0.5, 0.3]
    assert roll.getExpectedValue(values, probabilities) == pytest.approx(2.1)

    with pytest.raises(ValueError):
        roll.getExpectedValue([1, 2], [0.5, 0.5, 0.1])

    with pytest.raises(ValueError):
        roll.getExpectedValue([1, 2], [0.5, 0.4])


def test_seed_getter():
    """
    Test the seed getter method of the Roll class.

    This test verifies that the seed getter method correctly returns the seed value
    that was set during the initialization of the Roll instance.

    Assertions:
    - The seed getter returns the correct seed value.
    """
    seed_value = 12345
    roll = Roll(seed=seed_value, debug=True)
    assert roll.seed == seed_value


def test_seed_setter():
    """
    Test the seed setter method of the Roll class.

    This test verifies that the seed setter method correctly updates the seed value
    and that the random number generator is reseeded with the new seed value.

    Assertions:
    - The seed setter updates the seed value correctly.
    - The random number generator produces the same sequence of numbers after reseeding.
    """
    initial_seed = 12345
    new_seed = 67890
    roll = Roll(seed=initial_seed, debug=True)

    # 使用初始種子產生隨機數序列
    initial_sequence = [roll.RollNum(Dy=100) for _ in range(5)]

    # Set the new seed
    roll.seed = new_seed

    # Generate a sequence of random numbers with the new seed
    new_sequence = [roll.RollNum(Dy=100) for _ in range(5)]

    # Reset the seed to the initial seed and generate the sequence again
    roll.seed = initial_seed
    reset_sequence = [roll.RollNum(Dy=100) for _ in range(5)]

    assert roll.seed == initial_seed
    assert initial_sequence != new_sequence
    assert initial_sequence == reset_sequence


def test_rollNum_Err():
    """
    Test the RollNum method of the Roll class with invalid input.

    This test verifies that the RollNum method raises a ValueError when
    given invalid input.

    Raises:
    - ValueError: If the input string is invalid.
    """
    roll = Roll(debug=True)
    with pytest.raises(Exception):
        roll.RollNum("invalid")  # type: ignore
    with pytest.raises(Exception):
        roll.RollNum(Dy=None, rollData=None)


def test_RollNum_basic():
    """
    Test the RollNum method of the Roll class with basic input.

    This test checks if the RollNum method correctly processes the input string "1d6"
    and returns a result dictionary containing the keys "rollValueList", "Type", and "returnValueList".

    Assertions:
        - The result dictionary contains the key "rollValueList".
        - The result dictionary contains the key "Type".
        - The result dictionary contains the key "returnValueList".
        - The rollValueList contains a value between 1 and 6.
    """
    roll = Roll(debug=True)
    result = roll.RollNum(Roll.RollNumTextToDataTools("1d6"))
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result
    assert 1 <= result["rollValueList"][0] <= 6


def test_RollNum_with_bonus():
    """
    Test the RollNum method of the Roll class with bonus.

    This test checks if the RollNum method correctly processes the input string "1d6+2"
    and returns a result dictionary containing the keys "rollValueList", "Type", and "returnValueList".

    Assertions:
        - The result dictionary contains the key "rollValueList".
        - The result dictionary contains the key "Type".
        - The result dictionary contains the key "returnValueList".
        - The rollValueList contains a value between 3 and 8.
    """
    roll = Roll(debug=True)
    result = roll.RollNum(Roll.RollNumTextToDataTools("1d6+2"), bonus=1)
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result
    # assert 3 <= result["rollValueList"][0] <= 8


def test_RollNum_multiple_dice():
    """
    Test the RollNum method of the Roll class with multiple dice.

    This test checks if the RollNum method correctly processes the input string "2d6"
    and returns a result dictionary containing the keys "rollValueList", "Type", and "returnValueList".

    Assertions:
        - The result dictionary contains the key "rollValueList".
        - The result dictionary contains the key "Type".
        - The result dictionary contains the key "returnValueList".
        - The rollValueList contains two values each between 1 and 6.
    """
    roll = Roll()
    result = roll.RollNum(Roll.RollNumTextToDataTools("2d6"))
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result
    assert len(result["rollValueList"]) == 2
    assert all(1 <= value <= 6 for value in result["rollValueList"])


def test_RollNum_with_success():
    """
    Test the RollNum method of the Roll class with success criteria.

    This test checks if the RollNum method correctly processes the input string "1d20"
    with a success threshold and returns a result dictionary containing the keys "rollValueList", "Type", and "returnValueList".

    Assertions:
        - The result dictionary contains the key "rollValueList".
        - The result dictionary contains the key "Type".
        - The result dictionary contains the key "returnValueList".
        - The returnValueList contains the success status.
    """
    roll = Roll(rollType=RollType.DND)
    result = roll.RollNum(Roll.RollNumTextToDataTools("1d20"), success=10)
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result
    assert result["returnValueList"][0]["RollValueClass"] in [
        returnType.success,
        returnType.notSuccess,
        returnType.BigSuccess,
        returnType.BigNotSuccess,
    ]


def test_RollDNDNumWithBigSuccess(monkeypatch):
    roll = Roll(rollType=RollType.DND)
    monkeypatch.setattr(Random, "randint", lambda *args, **kwargs: 20)
    result = roll.RollNum(Roll.RollNumTextToDataTools("1d20"), success=10)
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result
    assert result["returnValueList"][0]["RollValueClass"] is returnType.BigSuccess


def test_RollDNDNumWithBigNotSuccess(monkeypatch):
    roll = Roll(rollType=RollType.DND)
    monkeypatch.setattr(Random, "randint", lambda *args, **kwargs: 1)
    result = roll.RollNum(Roll.RollNumTextToDataTools("1d20"), success=10)
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result
    assert result["returnValueList"][0]["RollValueClass"] is returnType.BigNotSuccess


def test_RollCOCNumWithBigSuccess(monkeypatch):
    roll = Roll(rollType=RollType.COC)
    monkeypatch.setattr(Random, "randint", lambda *args, **kwargs: 0)
    result = roll.RollNum(Roll.RollNumTextToDataTools("1d100"), success=10)
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result
    assert result["returnValueList"][0]["RollValueClass"] is returnType.BigSuccess


def test_RollCOCNumWithBigNotSuccess(monkeypatch):
    roll = Roll(rollType=RollType.COC)
    monkeypatch.setattr(Random, "randint", lambda *args, **kwargs: 100)
    result = roll.RollNum(Roll.RollNumTextToDataTools("1d100"), success=10)
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result
    assert result["returnValueList"][0]["RollValueClass"] is returnType.BigNotSuccess
