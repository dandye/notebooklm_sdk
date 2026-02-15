import os
import sys

# Add the parent directory to sys.path so it can find notebooklm_sdk
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from notebooklm_sdk import NotebookLMClient
from requests.exceptions import HTTPError

load_dotenv()

PROJECT_NUMBER = os.environ.get("NOTEBOOKLM_PROJECT_NUMBER", "")
LOCATION = os.environ.get("NOTEBOOKLM_LOCATION", "global")

def test():
    if not PROJECT_NUMBER:
        print("Error: NOTEBOOKLM_PROJECT_NUMBER is not set in the environment or .env file.")
        return

    client = NotebookLMClient(project_number=PROJECT_NUMBER, location=LOCATION)

    print("Creating notebook...")
    notebook = client.create_notebook(title="SDK Integration Test")
    
    notebook_id = notebook.get("notebookId", notebook["name"].split("/")[-1])
    print(f"Created notebook with ID: {notebook_id}")

    print("Uploading document...")
    # NOTE: user must provide a valid PDF to test it.
    file_path = "../sample.pdf"
    
    if not os.path.exists(file_path):
        print(f"Test PDF not found at {file_path}. Skipping upload.")
        return

    try:
        source = client.upload_document(
            notebook_id=notebook_id,
            file_path=file_path,
            display_name="math_norms_lecture.pdf" 
        )
    except HTTPError as e:
        print(f"Upload failed: {e.response.text}")
        return
        
    source_id = source["sourceId"]["id"]
    print(f"Uploaded source with ID: {source_id}")

    print("Checking document status...")
    status = client.get_document_status(notebook_id=notebook_id, source_id=source_id)
    print("Status:", status.get('settings', {}).get('status'))

if __name__ == "__main__":
    test()
