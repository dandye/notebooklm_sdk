# NotebookLM Enterprise SDK and MCP Server

This repository contains a Python SDK and an MCP Server for interacting with NotebookLM Enterprise via the Google Cloud Discovery Engine API.

## Features
- **Create Notebooks**: Programmatically generate new NotebookLM workspaces.
- **Upload Documents**: Stream bytes directly into NotebookLM sources.
- **Check Status**: Verify document parsing and token counts.

## Usage Environments

### 1. As a Gemini CLI Extension (Native Skills and Commands)
This package is fully configured as a Gemini CLI extension via `gemini-extension.json`. 

**Installation**
```bash
gemini extension install git https://github.com/YOUR_USERNAME/notebooklm_sdk.git
```
*Note: The interactive installation wizard will automatically prompt you for your `NOTEBOOKLM_PROJECT_NUMBER`.*

**Available Commands & Skills:**
- `create-notebooklm "Title"`: Create a new NotebookLM Notebook.
- `upload-notebooklm-doc <notebook_id> <file_path> <display_name>`: Upload a PDF document.
- `notebooklm-status <notebook_id> <source_id>`: Check processing status.

### 2. As an MCP Server (Claude Desktop / Remote MCP)
This package uses `FastMCP` to expose its tools via STDIO. 
Configure the MCP Client to execute `notebooklm-mcp`.

### 3. As a Standalone CLI / Python SDK
You can use the `notebooklm` Typer CLI directly in your terminal, or import `NotebookLMClient` from `notebooklm_sdk` to use within your own Python applications. It automatically loads variables from a `.env` file via `python-dotenv`.

## Development Notes
- The API explicitly requires the `/upload/v1alpha/` prefix when posting documents.
- Display names provided in document uploads are rigorously sanitized to alphanumeric characters or underscores, as providing characters like spaces reliably throws `INVALID_ARGUMENT` 400 errors from the Google API endpoints regardless of standard URL encoding.
- Ensure the executing environment has active Google Cloud credentials (`gcloud auth application-default login`).
