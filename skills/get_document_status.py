#!/usr/bin/env python3
"""
Description: Check the processing status of an uploaded document.
Usage: get_document_status.py <notebook_id> <source_id>
"""
import sys
import subprocess

if len(sys.argv) < 3:
    print("Usage: get_document_status.py <notebook_id> <source_id>")
    sys.exit(1)

notebook_id = sys.argv[1]
source_id = sys.argv[2]

# Delegate to the installed CLI tool
result = subprocess.run(
    ["notebooklm", "get-document-status", notebook_id, source_id],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)
