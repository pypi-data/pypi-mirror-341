from paul_tools.Tools import color, typeToColor

from .__init__ import pytest


def test_color():
    """
    Test the color function.
    """
    assert color("Hello", "World", color="red") == [
        "\x1b[31m",
        "Hello",
        "World",
        "\x1b[39m",
    ]
    assert color("Hello", "World") == ["Hello", "World"]
    with pytest.raises(ValueError):
        color("Hello", "World", color="invalid_color")


def test_typeToColor():
    """
    Test the typeToColor function.
    """
    assert typeToColor("ERROR") == "RED"
    assert typeToColor("ERR") == "RED"
    assert typeToColor("WARN") == "YELLOW"
    assert typeToColor("WARNING") == "YELLOW"
    assert typeToColor("info") == "INFO"
