import google.auth
from google.auth.transport.requests import Request
import requests
import re
from typing import Dict, Any, Optional
import urllib.parse
class NotebookLMClient:
    """
    Client for interacting with the NotebookLM Enterprise API 
    via Google Cloud Discovery Engine endpoints.
    """
    
    def __init__(self, project_number: str, location: str = "global"):
        """
        Args:
            project_number: The Google Cloud Project Number (e.g. 1234567890).
            location: The geographic location of the data store (e.g. 'global', 'us', 'eu').
        """
        self.project_number = project_number
        self.location = location
        self._endpoints_base = f"https://{self.location}-discoveryengine.googleapis.com/v1alpha/projects/{self.project_number}/locations/{self.location}/notebooks"
        self._upload_base = f"https://{self.location}-discoveryengine.googleapis.com/upload/v1alpha/projects/{self.project_number}/locations/{self.location}/notebooks"

    def _get_access_token(self) -> str:
        """Retrieves and refreshes the Google Auth access token."""
        credentials, _ = google.auth.default()
        if not credentials.valid:
            credentials.refresh(Request())
        return credentials.token

    def _get_auth_headers(self) -> Dict[str, str]:
        """Returns standard Authorization headers."""
        token = self._get_access_token()
        return {
            "Authorization": f"Bearer {token}"
        }

    def create_notebook(self, title: str) -> Dict[str, Any]:
        """
        Creates a new NotebookLM notebook.
        
        Args:
            title: The display title of the notebook.
            
        Returns:
            The created notebook definition object containing the notebookId.
        """
        headers = self._get_auth_headers()
        headers["Content-Type"] = "application/json"
        
        payload = {
            "title": title
        }
        
        response = requests.post(self._endpoints_base, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def upload_document(self, notebook_id: str, file_path: str, display_name: str, mime_type: str = "application/pdf") -> Dict[str, Any]:
        """
        Uploads a local file as a document (source) to the specified notebook.
        
        Args:
            notebook_id: The unique UUID of the target notebook.
            file_path: Local path to the file to upload.
            display_name: The name of the file to be displayed within NotebookLM.
                          Spaces and special characters will be URL-encoded automatically.
            mime_type: The content type of the file. Defaults to application/pdf.
            
        Returns:
            The created source definition object containing the sourceId.
        """
        endpoint = f"{self._upload_base}/{notebook_id}/sources:uploadFile"
        
        headers = self._get_auth_headers()
        safe_name = re.sub(r'[^\x20-\x7E]', '', display_name) # Remove non-ascii
        
        # When `test_sdk.py` failed even with safe names replacing everything, it meant something ELSE triggered 400.
        # Check `test_sdk.py`. Maybe notebook_id?
        # WAIT! In test_sdk.py: 
        # `notebook_id = notebook["name"].split("/")[-1]`
        # In the script `notebooklm_upload_final_v2.py`, NOTEBOOK_ID = "2b6a2c7b-53ea-4a59-a75d-e804114a4840" 
        # Let's print out what the SDK sent inside `test_sdk.py`!
        headers["X-Goog-Upload-File-Name"] = urllib.parse.quote(safe_name)
        headers["X-Goog-Upload-Protocol"] = "raw"
        headers["Content-Type"] = mime_type
        
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            
        response = requests.post(endpoint, headers=headers, data=file_bytes)
        response.raise_for_status()
        return response.json()

    def get_document_status(self, notebook_id: str, source_id: str) -> Dict[str, Any]:
        """
        Retrieves the status and metrics (word count, token count) of an uploaded document.
        
        Args:
            notebook_id: The unique UUID of the notebook.
            source_id: The unique UUID of the uploaded source document.
            
        Returns:
            The source definition block. Check `settings.status` for 'SOURCE_STATUS_COMPLETE'.
        """
        endpoint = f"{self._endpoints_base}/{notebook_id}/sources/{source_id}"
        
        headers = self._get_auth_headers()
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
