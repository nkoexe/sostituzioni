from datetime import datetime
from pathlib import Path
from shutil import copyfile
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import googleapiclient.discovery
import logging

from sostituzioni.control.configurazione import configurazione


logger = logging.getLogger(__name__)


def backup():
    database_file = configurazione.get("databasepath").path
    backup_dir = configurazione.get("backupdir").path

    if not database_file.is_file():
        return FileNotFoundError(f"Database file {database_file} not found.")

    if not backup_dir.is_dir():
        backup_dir.mkdir()

    database_name = database_file.stem
    database_ext = database_file.suffix
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_file = backup_dir / f"backup_{database_name}_{date}{database_ext}"

    logger.debug(f"Backing up database to {backup_file}")

    copyfile(database_file, backup_file)

    logger.debug("Uploading backup to Google Drive..")
    upload_to_drive(backup_file)

    logger.info("Backup completed successfully.")

    return backup_file


def upload_to_drive(backup_file):
    file_name = str(backup_file.name)
    folder_id = configurazione.get("backupdrivefolderid")

    metadata = {"name": file_name, "parents": [folder_id] if folder_id else []}

    media = MediaFileUpload(backup_file, resumable=True)

    credentials = service_account.Credentials.from_service_account_file(
        Path(__file__).parent / "sostituzioni-test-14b8b9ffec37.json",
        scopes=["https://www.googleapis.com/auth/drive.file"],
    )

    drive_service = googleapiclient.discovery.build(
        "drive", "v3", credentials=credentials
    )

    file = (
        drive_service.files()
        .create(body=metadata, media_body=media, fields="id")
        .execute()
    )

    logger.debug(f"File uploaded with ID: {file['id']}")
    return file["id"]
