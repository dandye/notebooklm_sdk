from mcp.server.fastmcp import FastMCP
from notebooklm_sdk.client import NotebookLMClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP Server
mcp = FastMCP("NotebookLM Enterprise")

# Fetch credentials from environment
PROJECT_NUMBER = os.environ.get("NOTEBOOKLM_PROJECT_NUMBER", "")
LOCATION = os.environ.get("NOTEBOOKLM_LOCATION", "global")

client = NotebookLMClient(project_number=PROJECT_NUMBER, location=LOCATION)

@mcp.tool()
def create_notebook(title: str) -> str:
    """
    Creates a new NotebookLM notebook.
    
    Args:
        title: The display title of the notebook.
    """
    notebook = client.create_notebook(title=title)
    notebook_id = notebook.get("notebookId", notebook.get("name", "").split("/")[-1])
    return f"Notebook created successfully with ID: {notebook_id}"

@mcp.tool()
def upload_document(notebook_id: str, file_path: str, display_name: str) -> str:
    """
    Uploads a local file as a document (source) to the specified NotebookLM notebook.
    
    Args:
        notebook_id: The unique UUID of the target notebook.
        file_path: Local absolute path to the file to upload.
        display_name: The name of the file to be displayed within NotebookLM.
    """
    source = client.upload_document(
        notebook_id=notebook_id, 
        file_path=file_path, 
        display_name=display_name
    )
    source_id = source["sourceId"]["id"]
    return f"Document uploaded successfully with Source ID: {source_id}"

@mcp.tool()
def get_document_status(notebook_id: str, source_id: str) -> str:
    """
    Retrieves the processing status and metrics (word count, token count) of an uploaded document.
    
    Args:
        notebook_id: The unique UUID of the notebook.
        source_id: The unique UUID of the uploaded source document.
    """
    status = client.get_document_status(notebook_id=notebook_id, source_id=source_id)
    
    current_status = status.get('settings', {}).get('status', 'UNKNOWN')
    metrics = status.get('metadata', {})
    
    return f"Status: {current_status}\nMetrics: {metrics}"

def main():
    """Entry point for the notebooklm-mcp command."""
    if not PROJECT_NUMBER:
        print("Error: NOTEBOOKLM_PROJECT_NUMBER environment variable is not set.", flush=True)
        import sys
        sys.exit(1)
    mcp.run()

if __name__ == "__main__":
    main()
