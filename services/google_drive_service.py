import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from ..utils.logger import logger
from ..utils.google_auth_flow import google_auth_flow

class GoogleDriveService:
    def __init__(self):
        pass

    def _get_drive_service(self, refresh_token: str):
        creds = google_auth_flow.get_credentials(refresh_token)
        return build("drive", "v3", credentials=creds)

    def find_or_create_folder(self, refresh_token: str, folder_name: str) -> str:
        service = self._get_drive_service(refresh_token)
        
        # Search for the folder
        query = f"name=\\'{folder_name}\\' and mimeType=\\'application/vnd.google-apps.folder\\' and trashed=false"
        results = service.files().list(q=query, spaces=\'drive\', fields=\'files(id, name)\').execute()
        items = results.get(\'files\', [])

        if items:
            logger.info(f"Found existing folder: {items[0][\'name\']} ({items[0][\'id\]})")
            return items[0][\'id\']
        else:
            logger.info(f"Folder \'{folder_name}\' not found. Creating new folder.")
            file_metadata = {
                \'name\': folder_name,
                \'mimeType\': \'application/vnd.google-apps.folder\'
            }
            folder = service.files().create(body=file_metadata, fields=\'id\').execute()
            logger.info(f"Created new folder: {folder_name} ({folder.get(\'id\')})")
            return folder.get(\'id\')

    def upload_file(self, refresh_token: str, file_path: str, folder_id: str) -> str:
        service = self._get_drive_service(refresh_token)
        file_name = os.path.basename(file_path)
        file_metadata = {
            \'name\': file_name,
            \'parents\': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields=\'id, webContentLink\').execute()
        logger.info(f"Uploaded file {file_name} ({file.get(\'id\')}) to folder {folder_id}")
        return file.get(\'webContentLink\') # Returns a direct download link if available, or a view link

google_drive_service = GoogleDriveService()

