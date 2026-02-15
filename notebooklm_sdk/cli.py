import typer
import os
import sys
from dotenv import load_dotenv
from notebooklm_sdk.client import NotebookLMClient

# Load environment variables
load_dotenv()

app = typer.Typer(help="NotebookLM Enterprise CLI")

def get_client() -> NotebookLMClient:
    project_number = os.environ.get("NOTEBOOKLM_PROJECT_NUMBER", "")
    if not project_number:
        typer.echo("Error: NOTEBOOKLM_PROJECT_NUMBER environment variable is not set.", err=True)
        sys.exit(1)
        
    location = os.environ.get("NOTEBOOKLM_LOCATION", "global")
    return NotebookLMClient(project_number=project_number, location=location)

@app.command()
def create_notebook(title: str = typer.Argument(..., help="The title of the new notebook")):
    """Create a new NotebookLM notebook."""
    client = get_client()
    try:
        notebook = client.create_notebook(title=title)
        notebook_id = notebook.get("notebookId", notebook.get("name", "").split("/")[-1])
        typer.echo(f"Notebook created successfully!")
        typer.echo(f"ID: {notebook_id}")
    except Exception as e:
        typer.echo(f"Error creating notebook: {e}", err=True)

@app.command()
def upload_document(
    notebook_id: str = typer.Argument(..., help="The UUID of the target notebook"),
    file_path: str = typer.Argument(..., help="Path to the local file to upload"),
    display_name: str = typer.Argument(..., help="Name to display in NotebookLM")
):
    """Upload a document to an existing NotebookLM notebook."""
    client = get_client()
    try:
        source = client.upload_document(notebook_id=notebook_id, file_path=file_path, display_name=display_name)
        source_id = source.get("sourceId", {}).get("id", "Unknown")
        typer.echo(f"Document uploaded successfully!")
        typer.echo(f"Source ID: {source_id}")
    except Exception as e:
        typer.echo(f"Error uploading document: {e}", err=True)

@app.command()
def get_document_status(
    notebook_id: str = typer.Argument(..., help="The UUID of the notebook"),
    source_id: str = typer.Argument(..., help="The UUID of the source document")
):
    """Check the processing status of an uploaded document."""
    client = get_client()
    try:
        status = client.get_document_status(notebook_id=notebook_id, source_id=source_id)
        current_status = status.get('settings', {}).get('status', 'UNKNOWN')
        metadata = status.get('metadata', {})
        typer.echo(f"Status: {current_status}")
        typer.echo(f"Word Count: {metadata.get('wordCount', 'N/A')}")
        typer.echo(f"Token Count: {metadata.get('tokenCount', 'N/A')}")
    except Exception as e:
        typer.echo(f"Error getting document status: {e}", err=True)

def main():
    app()

if __name__ == "__main__":
    main()
