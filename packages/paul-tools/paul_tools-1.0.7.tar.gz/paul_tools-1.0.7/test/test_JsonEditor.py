import json

from paul_tools.JsonEditor import JsonEditor

from .__init__ import pytest


class TestJsonEditor:
    @pytest.fixture
    def json_editor(self, tmp_path):
        # Create a temporary directory and file for testing
        temp_dir = tmp_path / "json_files"
        temp_dir.mkdir()
        temp_file = temp_dir / "test.json"
        temp_file.write_text("{}")
        return JsonEditor(path=temp_file)

    def test_init(self, json_editor: JsonEditor, tmp_path):
        assert json_editor.jsonDict == {}
        assert tmp_path / "json_files" / "test.json" == json_editor.jsonPath

    def test_write_json(self, json_editor: JsonEditor, tmp_path):
        json_editor.jsonDict = {"key": "value"}
        json_editor.write_json()
        with open(json_editor.jsonPath, "rt", encoding="utf-8") as f:
            data = json.load(f)
        assert data == {"key": "value"}

    def test_del_from_key(self, json_editor: JsonEditor):
        json_editor.jsonDict = {"key": "value"}
        json_editor.del_from_key("key")
        assert "key" not in json_editor.jsonDict

    def test_edit(self, monkeypatch, json_editor: JsonEditor):
        inputs = iter(
            [
                "key='value'",
                "key",
                "save",
                "del key",
                "key2='value2'",
                "del",
                "key2",
                "",
                "EOF",
                "^Z",
                "exit",
            ]
        )
        monkeypatch.setattr("builtins.input", lambda _: next(inputs, None))
        json_editor.edit()
        assert json_editor.jsonDict == {}

    def test_pathIsNone(self, monkeypatch, tmpdir):
        inputs = iter([str(tmpdir / "test2.json"), "exit"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs, None))
        JsonEditor()

    def test_Err(self, monkeypatch, json_editor: JsonEditor):
        def err(*args, **kwargs):
            raise EOFError

        monkeypatch.setattr("builtins.input", err)
        json_editor.edit()
