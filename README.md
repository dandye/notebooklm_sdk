# NotebookLM SDK

A Python client for interacting with the NotebookLM Enterprise API via Google Cloud Discovery Engine REST endpoints.

## Installation

You can install this SDK manually or via `pip`:

```bash
pip install -e .
```

## Usage

This SDK relies on [Google Cloud Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials). Before running, ensure your credentials and projects are set up:

```bash
gcloud auth application-default login
gcloud config set project [YOUR_PROJECT_ID]
```

### Example

```python
from notebooklm_sdk import NotebookLMClient
import time

PROJECT_NUMBER = "1234567890"  # Replace with your GCP project number
LOCATION = "global"

client = NotebookLMClient(project_number=PROJECT_NUMBER, location=LOCATION)

# 1. Create a Notebook
print("Creating notebook...")
notebook = client.create_notebook(title="Test SDK Notebook")
notebook_id = notebook["notebookId"]
print(f"Created notebook with ID: {notebook_id}")

# 2. Upload a File
print("Uploading document...")
# This automatically handles URL-encoding the display name to avoid 400 errors.
source = client.upload_document(
    notebook_id=notebook_id,
    file_path="m3_cai5031_lecture1_norms.pdf",
    display_name="Math Norms Lecture via SDK"
)
source_id = source["sourceId"]["id"]
print(f"Uploaded source with ID: {source_id}")

# 3. Check Status
print("Checking document status...")
status = client.get_document_status(notebook_id=notebook_id, source_id=source_id)
print(status)
```

## MCP Server

This SDK also includes an integrated [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server, which allows AI agents and clients (like Claude Desktop) to natively call NotebookLM methods as tools.

### Running the MCP server

Once the package is installed, you can start the MCP server via `stdio`:

```bash
notebooklm-mcp
```

### Configuring Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "notebooklm-mcp",
      "env": {
        "NOTEBOOKLM_PROJECT_NUMBER": "813924125873",
        "NOTEBOOKLM_LOCATION": "global"
      }
    }
  }
}
```
Ensure that the `notebooklm-mcp` executable is available in your PATH, or provide the absolute path to your virtual environment's binary (e.g., `/path/to/.venv/bin/notebooklm-mcp`). You will also need active application default credentials.

## Typer CLI

There is also a standard Typer CLI command for human operation. To use it, simply run:

```bash
notebooklm --help
```

You can pass authentication details via a `.env` file containing:
```
NOTEBOOKLM_PROJECT_NUMBER=your_project_number
NOTEBOOKLM_LOCATION=your_location
```
