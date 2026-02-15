---
name: create-notebooklm
description: Create a NotebookLM Notebook
slash_command: /notebooklm:create
personas:
  - knowledge_worker
triggers:
  - "create a new notebook"
  - "initialize a workspace"
---
# Create NotebookLM Notebook

This skill allows you to create a new NotebookLM workspace notebook using the NotebookLM SDK.

1.  Use the MCP Server `notebooklm` tool `create_notebook(title: str)` to provision the notebook.
2.  Alternatively, you can run the CLI command:
    ```bash
    uv run notebooklm create-notebook "Notebook Title"
    ```
