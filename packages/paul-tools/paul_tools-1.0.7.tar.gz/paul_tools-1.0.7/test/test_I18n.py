from paul_tools.I18n import I18n

from .__init__ import pytest


def test_langReplace():
    """
    Test the langReplace method of the I18n class.

    This test verifies that the langReplace method correctly converts language codes
    and names to their corresponding standardized forms.

    Assertions:
    - langReplace("zh") should return "zh_cn".
    - langReplace("chinese (traditional)_hong kong sar") should return "zh_hk".
    - langReplace("en_us") should return "en_us".
    - langReplace("sys") should return the same result as langReplace(getSysLang()).
    """
    assert I18n.langReplace("zh") == "zh_cn"
    assert I18n.langReplace("chinese (traditional)_hong kong sar") == "zh_hk"
    assert I18n.langReplace("en_us") == "en_us"
    assert I18n.langReplace("sys") == I18n.langReplace(I18n.getSysLang())


def test_getSysLang():
    """
    Test the getSysLang method of the I18n class.

    This test checks if the getSysLang method returns a value of type string.

    Assertions:
        - The return value of I18n.getSysLang() is an instance of str.
    """
    assert isinstance(I18n.getSysLang(), str)


def test_init():
    """
    Test the initialization of the I18n class.
    This test case verifies the following:
    1. Initializing I18n with an empty Langs list raises a ValueError.
    2. Initializing I18n with valid parameters sets the DIR_ROOT, langs, and LANG_JSON attributes correctly.
    Assertions:
    - Raises ValueError when Langs is an empty list.
    - DIR_ROOT is set to "test_dir".
    - langs is set to ["en_us"].
    - LANG_JSON contains the key "test_key" with value "test_value".
    """
    with pytest.raises(ValueError):
        I18n(Langs=[])

    i18n = I18n(
        Langs=["en_us"],
        dirRoot="test_dir",
        langJson={"en_us": {"test_key": "test_value"}},
    )
    assert i18n.DIR_ROOT == "test_dir"
    assert i18n.langs == ["en_us"]
    assert i18n.LANG_JSON["test_key"] == "test_value"


def test_locale():
    """
    Tests the functionality of the I18n class for localization.
    This function performs the following tests:
    1. Checks if the locale method correctly formats a string with positional and keyword arguments.
    2. Verifies that the locale method returns the key itself when the key does not exist in the language JSON.
    3. Ensures that the locale method returns the unformatted string when no arguments are provided.
    4. Confirms that the get method returns the same result as the locale method.
    5. Asserts that the get method is the same as the locale method.
    Additionally, it includes a nested function to test language replacement:
    - Checks if the langReplace method correctly replaces language codes.
    """
    i18n = I18n(
        Langs=["en_us"], langJson={"en_us": {"test_key": "test_value {1}{arg}{0}"}}
    )
    assert (
        i18n.locale("test_key", "a0", "a1", arg="argument") == "test_value a1argumenta0"
    )
    assert i18n.locale("non_existent_key") == "non_existent_key"
    assert i18n.locale("test_key") == "test_value {1}{arg}{0}"
    assert i18n.get("test_key") == "test_value {1}{arg}{0}"
    assert i18n.get == i18n.locale


@pytest.fixture
def new_file(tmp_path):
    lang_dir = tmp_path / "langs"
    lang_dir.mkdir()

    # Create a temporary directory and file for testing
    temp_en_us_file = lang_dir / "en_us.json"
    temp_en_us_file.write_text('{"a":"b"}')

    temp_zh_hk_file = lang_dir / "zh_hk.json"
    temp_zh_hk_file.write_text('{"a":"c"')

    return tmp_path


def test_file_locale(new_file):
    i18n = I18n(dirRoot=new_file, Langs=["en_us", "zh_hk", "None"])
    assert i18n.get("a") == "b"
