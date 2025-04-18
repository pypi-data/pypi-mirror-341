# paul-tools

一個簡單的 lib，提供多種實用工具和功能模塊。

## 功能模塊

- **I18n**: 提供國際化和本地化支持。
- **Roll**: 支持多種骰子擲點規則的模塊。
- **JsonEditor**: 用於操作 JSON 文件的工具。
- **Decorator**: 包含多種裝飾器，例如 `debug`、`getTime`、`noPrint` 和 `retry`。
- **Tools**: 提供通用工具函數。
- **good_list**: 自定義的列表類，支持額外的操作方法。

## 開發指南

```bash
poetry install
pip install pytest pytest-cov
pytest test
```

## 測試

本項目包含單元測試，位於 `test/` 目錄下。使用 `pytest` 運行測試以確保代碼的正確性和穩定性。
