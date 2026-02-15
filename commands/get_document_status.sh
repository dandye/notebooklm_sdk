#!/bin/bash
# Description: Get the status of an uploaded document in NotebookLM
# Usage: uv run notebooklm get-document-status <notebook_id> <source_id>

if [ "$#" -ne 2 ]; then
    echo "Usage: uv run notebooklm get-document-status <notebook_id> <source_id>"
    exit 1
fi

uv run notebooklm get-document-status "$1" "$2"
