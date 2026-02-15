---
name: notebooklm-status
description: Check the processing status of a NotebookLM document
slash_command: /notebooklm:status
personas:
  - knowledge_worker
triggers:
  - "is my document done processing?"
  - "status of notebook source"
---
# Get Document Status

NotebookLM processes documents asynchronously to extract entities and generate summaries. Use this skill to check if a document is fully ingested (`SOURCE_STATUS_COMPLETE`).

1.  Use the MCP Server `notebooklm` tool `get_document_status(notebook_id: str, source_id: str)`.
2.  Alternatively, use the CLI command:
    ```bash
    uv run notebooklm get-document-status <notebook_id> <source_id>
    ```
