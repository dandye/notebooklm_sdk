#!/usr/bin/env python3
"""
Description: Upload a document to an existing NotebookLM notebook.
Usage: upload_document.py <notebook_id> <file_path> <display_name>
"""
import sys
import subprocess

if len(sys.argv) < 4:
    print("Usage: upload_document.py <notebook_id> <file_path> <display_name>")
    sys.exit(1)

notebook_id = sys.argv[1]
file_path = sys.argv[2]
display_name = sys.argv[3]

# Delegate to the installed CLI tool
result = subprocess.run(
    ["uv", "run", "notebooklm", "upload-document", notebook_id, file_path, display_name],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)
