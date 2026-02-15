# NotebookLM Enterprise SDK and MCP Server

This repository contains a Python SDK and an MCP Server for interacting with NotebookLM Enterprise via the Google Cloud Discovery Engine API.

## Features
- **Create Notebooks**: Programmatically generate new NotebookLM workspaces.
- **Upload Documents**: Stream bytes directly into NotebookLM sources.
- **Check Status**: Verify document parsing and token counts.

## Usage Environments

### 1. As a Python SDK
You can import the `NotebookLMClient` from `notebooklm_sdk` to use within your own Python applications.

### 2. As an MCP Server (Gemini CLI / Claude Desktop)
This package uses `FastMCP` to expose its tools via STDIO. 
When used with the Gemini CLI, the `gemini-extension.json` ensures you are seamlessly prompted for the required `NOTEBOOKLM_PROJECT_NUMBER` environment variable via the ConfigWizard.

### 3. As a Standalone CLI
You can use the `notebooklm` command line utility directly in your terminal for manual operations. It automatically loads variables from a `.env` file via `python-dotenv`.

## Development Notes
- The API explicitly requires the `/upload/v1alpha/` prefix when posting documents.
- Display names provided in document uploads are rigorously sanitized to alphanumeric characters or underscores, as providing characters like spaces reliably throws `INVALID_ARGUMENT` 400 errors from the Google API endpoints regardless of standard URL encoding.
- Ensure the executing environment has active Google Cloud credentials (`gcloud auth application-default login`).
