---
description: Upload a document to a NotebookLM Notebook
---
# Upload Document to NotebookLM

This skill allows you to upload local files (e.g. PDFs) directly into a NotebookLM Notebook source.

1.  Use the MCP Server `notebooklm` tool `upload_document(notebook_id: str, file_path: str, display_name: str)` to upload the document.
2.  Alternatively, you can run the CLI command:
    ```bash
    uv run notebooklm upload-document <notebook_id> <file_path> "Display Name"
    ```
