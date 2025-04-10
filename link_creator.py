from __future__ import print_function
import os
import pickle
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from supabase import create_client, Client

# Use read-only scope for accessing files.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    """
    Authenticates the user using OAuth 2.0.
    Credentials are stored in token.pickle for future runs.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_pdf_links_by_folder(service):
    """
    Searches Google Drive for all PDF files.
    For each PDF file, retrieves its parent's folder name (used here as course code)
    and maps that folder name to a list of shareable PDF links.
    
    Returns:
        A dictionary where keys are course codes (folder names)
        and values are lists of shareable PDF links.
    """
    pdf_by_folder = {}
    page_token = None
    query = "mimeType='application/pdf'"
    
    # Cache to reduce repeated API calls for the same folder.
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
            # Build the shareable preview link for the PDF file.
            file_link = f"https://drive.google.com/file/d/{file_id}/preview"
            
            # Try to use the parent folder name as the course code.
            parents = file.get('parents', [])
            if parents:
                parent_id = parents[0]
                if parent_id in folder_cache:
                    course_code = folder_cache[parent_id]
                else:
                    try:
                        parent_info = service.files().get(
                            fileId=parent_id,
                            fields="name, mimeType"
                        ).execute()
                        # Confirm the parent is a folder before using its name.
                        if parent_info.get('mimeType') == 'application/vnd.google-apps.folder':
                            course_code = parent_info.get('name')
                        else:
                            course_code = file.get('name')  # fallback
                        folder_cache[parent_id] = course_code
                    except Exception as e:
                        print(f"Error retrieving folder info for parent ID {parent_id}: {e}")
                        course_code = file.get('name')
            else:
                # If no parent exists, use the file's name.
                course_code = file.get('name')
            
            # Append the PDF link to the list for this course code.
            pdf_by_folder.setdefault(course_code, []).append(file_link)
        
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break

    return pdf_by_folder

def export_to_json(data, filename="pdf_links_import.json"):
    """
    Exports the provided dictionary data to a JSON file.
    
    Args:
        data: Dictionary containing PDF links by course code.
        filename: The output filename (default: pdf_links_import.json).
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Data exported to {filename}")

def get_existing_course_codes(supabase: Client):
    """
    Retrieves all existing course codes from the Supabase 'courses_new' table.
    
    Returns:
        A set of course codes that exist in Supabase.
    """
    offset = 0
    limit = 1000
    course_codes = set()
    while True:
        response = supabase.table("courses_new").select("course_code") \
                         .range(offset, offset + limit - 1).execute()
        data = response.data
        if not data:
            break
        for row in data:
            course_codes.add(row["course_code"])
        offset += limit
    return course_codes

def main():
    # Initialize the Supabase client using credentials from a config file.
    with open(".venv\\config.json", "r") as file:
        config = json.load(file)
    url = config["SUPABASE_URL"]
    key = config["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    # Authenticate with Google and build the Drive API service.
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Retrieve all PDF links and export them as JSON.
    pdf_links = get_pdf_links_by_folder(service)
    if not pdf_links:
        print("No PDF files found in your drive.")
    else:
        export_to_json(pdf_links)

    # Load the PDF links from the exported JSON file.
    with open("pdf_links_import.json", "r") as import_file:
        pdf_links_import = json.load(import_file)

    # Retrieve all existing course codes from Supabase.
    existing_courses = get_existing_course_codes(supabase)
    

    # For each course in the JSON data, update the 'pdf_links' field in Supabase only if the course exists.
    for course, links in pdf_links_import.items():
        if course in existing_courses:
            print(f"Updating course: {course} with PDF links: {links}")
            response = supabase.table("courses_new").update({"pdf_links": links}).eq("course_code", course).execute()
            print("Supabase response:", response)
        else:
            print(f"Course code '{course}' not found in Supabase. Skipping update for this course.")

    # Optionally, fetch and print updated data from Supabase for verification.
    updated_response = supabase.table("courses_new").select("course_code, pdf_links").execute()
    if updated_response.data:
        print("First record in courses_new table after update:", updated_response.data[0])
    else:
        print("No records found in courses_new table.")

if __name__ == '__main__':
    main()
