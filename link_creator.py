from __future__ import print_function
import os
import pickle
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Use read-only scope for accessing files.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """
    Handles user authentication using OAuth 2.0.
    Credentials are stored in token.pickle for future runs.
    """
    creds = None
    # Check if token.pickle exists.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials are available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # credentials.json must be present in the same directory.
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_all_pdf_links(service):
    """
    Searches the drive for all PDF files and returns a list of tuples.
    Each tuple consists of (course_code, shareable_link) where course_code is
    obtained from the parent folder of the PDF.
    """
    pdf_files = []
    page_token = None
    # The query finds files with the PDF MIME type.
    query = "mimeType='application/pdf'"
    # Cache to avoid multiple API calls for the same folder.
    folder_cache = {}
    
    while True:
        response = service.files().list(
            q=query,
            spaces='drive',
            fields="nextPageToken, files(id, name, parents)",
            pageToken=page_token
        ).execute()
        
        for file in response.get('files', []):
            file_id = file['id']
            # Try to get the parent folder ID; a file can be in multiple folders.
            parents = file.get('parents', [])
            if parents:
                parent_id = parents[0]
                # Check if we already looked up this folder.
                if parent_id in folder_cache:
                    course_code = folder_cache[parent_id]
                else:
                    try:
                        parent_info = service.files().get(
                            fileId=parent_id,
                            fields="name, mimeType"
                        ).execute()
                        # Verify that the parent is really a folder.
                        if parent_info.get('mimeType') == 'application/vnd.google-apps.folder':
                            course_code = parent_info.get('name')
                        else:
                            course_code = file.get('name')
                        folder_cache[parent_id] = course_code
                    except Exception as e:
                        print(f"Error retrieving folder info for parent ID {parent_id}: {e}")
                        course_code = file.get('name')
            else:
                # If no parent is found, fallback on the file's name.
                course_code = file.get('name')
            
            # Build the shareable link using the file ID.
            file_link = f"https://drive.google.com/file/d/{file_id}/preview"
            pdf_files.append((course_code, file_link))
        
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return pdf_files

def main():
    # Authenticate and build the Google Drive API service.
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Retrieve all PDF files with folder names.
    pdf_links = get_all_pdf_links(service)
    if not pdf_links:
        print("No PDF files found in your drive.")
    else:
        print("List of PDF files (labeled with their folder names) and their shareable links:\n")
        for course_code, link in pdf_links:
            print(f"course_code: {course_code}")
            print(f"pdf_links: {link}\n")

if __name__ == '__main__':
    main()
