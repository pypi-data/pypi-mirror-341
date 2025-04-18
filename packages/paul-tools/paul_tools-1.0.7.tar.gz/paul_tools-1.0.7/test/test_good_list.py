from paul_tools.good_list import list

from .__init__ import pytest


def test_join():
    assert list(["a", "b", "c"]).join(",") == "a,b,c"
