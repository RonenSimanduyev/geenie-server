import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload




def uploadToSheets(asin: str):
    csv_file_path = asin
    # Set the path to your CSV file

    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Set the credentials of your Google account
    creds = Credentials.from_authorized_user_file('credentials.json', scopes=SCOPES)

    # Create a Google Drive API client
    drive_service = build('drive', 'v3', credentials=creds)

    # Upload file to Google Drive
    folder_id = '1bcwnn69fzFm5XoloedrnBCk-gWR5XXJ3'
    file_metadata = {'name': f'{asin}', 'parents':[folder_id]}
    media = MediaFileUpload(csv_file_path, mimetype='text/csv')
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Set the appropriate permissions on the uploaded file
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    drive_service.permissions().create(
        fileId=file['id'],
        body=permission,
        sendNotificationEmail=False,
    ).execute()

    # Get the URL of the uploaded file
    file_url = f'https://drive.google.com/file/d/{file["id"]}/view?usp=sharing'

    # Print the URL of the uploaded file
    return f'Shareable file URL: {file_url}'


def remove_scrapper_result(asin: str):
    csv_file_path = asin

    # Close the file and delete it from local directory
    with open(csv_file_path, 'r') as f:
        pass
    os.remove(csv_file_path)
