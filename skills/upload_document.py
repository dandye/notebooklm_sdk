#!/usr/bin/env python3
"""
Description: Upload a document to an existing NotebookLM notebook.
Usage: upload_document.py <notebook_id> <file_path> <display_name>
"""
import sys
import os
import json

# Add the parent directory to sys.path so it can find notebooklm_sdk natively
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from notebooklm_sdk.client import NotebookLMClient
from requests.exceptions import HTTPError

def main():
    load_dotenv()

    if len(sys.argv) < 4:
        print("Usage: upload_document.py <notebook_id> <file_path> <display_name>", file=sys.stderr)
        sys.exit(1)

    notebook_id = sys.argv[1]
    file_path = sys.argv[2]
    display_name = sys.argv[3]

    project_number = os.environ.get("NOTEBOOKLM_PROJECT_NUMBER", "")
    location = os.environ.get("NOTEBOOKLM_LOCATION", "global")

    if not project_number:
        print("Error: NOTEBOOKLM_PROJECT_NUMBER environment variable is not set.", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(file_path):
        print(f"Error: Provided file path does not exist: {file_path}", file=sys.stderr)
        sys.exit(1)

    client = NotebookLMClient(project_number=project_number, location=location)

    try:
        response = client.upload_document(notebook_id, file_path, display_name)
        print(json.dumps(response, indent=2))
    except HTTPError as e:
        print(f"Error uploading document: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
