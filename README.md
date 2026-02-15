# NotebookLM SDK

A Python client, Typer CLI, MCP Server, and Gemini Extension for interacting with the NotebookLM Enterprise API via Google Cloud Discovery Engine REST endpoints.

## Gemini CLI Extension Installation

This SDK doubles as a native [Gemini CLI](https://github.com/GoogleCloudPlatform/gemini-cli) extension. The extension will automatically configure the required environment variables.

1. **Install the Extension via Git:**
   ```bash
   gemini extension install git https://github.com/YOUR_USERNAME/notebooklm_sdk.git
   ```

2. **Configuration Prompts:**
   During the installation, the Gemini CLI wizard will automatically prompt you to fill in the following configuration variables required by the extension:
   - `NOTEBOOKLM_PROJECT_NUMBER`: Your Google Cloud Project Number where NotebookLM is hosted.
   - `NOTEBOOKLM_LOCATION`: The target region (defaults to `global`).

Once installed, you can use commands natively via the CLI (e.g., `gemini run create-notebooklm`).

---

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

### Python SDK Example

```python
from notebooklm_sdk import NotebookLMClient

PROJECT_NUMBER = "1234567890"  # Replace with your GCP project number
LOCATION = "global"

client = NotebookLMClient(project_number=PROJECT_NUMBER, location=LOCATION)

# 1. Create a Notebook
notebook = client.create_notebook(title="My Research SDK Notebook")
notebook_id = notebook.get("notebookId")
print(f"Created notebook with ID: {notebook_id}")

# 2. Upload a File
source = client.upload_document(
    notebook_id=notebook_id,
    file_path="research_paper.pdf",
    display_name="math_research_v1.pdf"
)
source_id = source["sourceId"]["id"]
print(f"Uploaded document with Source ID: {source_id}")

# 3. Check Status
status = client.get_document_status(notebook_id=notebook_id, source_id=source_id)
print(f"Document parsing status: {status['settings']['status']}")
```

---

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

---

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
        "NOTEBOOKLM_PROJECT_NUMBER": "YOUR_PROJECT_NUMBER",
        "NOTEBOOKLM_LOCATION": "global"
      }
    }
  }
}
```
Ensure that the `notebooklm-mcp` executable is available in your PATH, or provide the absolute path to your virtual environment's binary (e.g., `/path/to/.venv/bin/notebooklm-mcp`). You will also need active application default credentials.
