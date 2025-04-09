from __future__ import print_function
import os
import io
import pickle
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from PyPDF2 import PdfReader

# If modifying these scopes, delete the file token.pickle.
# The scope 'drive.readonly' is enough for listing and exporting file content.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """Handles authentication and returns valid credentials."""
    creds = None
    # token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # credentials.json should be your OAuth 2.0 Client IDs file.
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def view_pdf(service, file_id, file_name):
    """
    Downloads the PDF file from Google Drive using its file ID,
    then uses PyPDF2 to extract and print its content.
    """
    # Request to get the media (content) of the file.
    request = service.files().get_media(fileId=file_id)
    # Prepare an in-memory bytes buffer to hold the downloaded file.
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    print(f"Downloading {file_name}...")
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download progress: {int(status.progress()*100)}%")
    # Move back to the beginning of the BytesIO buffer.
    fh.seek(0)
    # Read PDF content using PyPDF2.
    reader = PdfReader(fh)
    print(f"\n--- Content of {file_name} ---")
    for page in reader.pages:
        text = page.extract_text()
        if text:
            print(text)
    print(f"--- End of {file_name} ---\n")

def list_and_view_files(service, folder_id):
    """
    Lists all files in the specified folder.
    For files that are PDFs, download and view their content.
    """
    # Query files in the given folder (folder_id).
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        print("No files found in the folder.")
        return

    for item in items:
        print(f"Found file: {item['name']} (ID: {item['id']}) - {item['mimeType']}")
        if item['mimeType'] == 'application/pdf':
            try:
                view_pdf(service, item['id'], item['name'])
            except Exception as e:
                print(f"Error processing {item['name']}: {e}\n")
        else:
            print(f"Skipping {item['name']}: Not a PDF file.\n")

def main():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    
    # Replace with your actual folder ID.
    folder_id = "1WRS1INYJWZP06g6i1OpF1M_TRmKquR0v"
    list_and_view_files(service, folder_id)

if __name__ == '__main__':
    main()
