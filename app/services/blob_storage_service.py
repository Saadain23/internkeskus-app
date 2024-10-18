from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import ResourceExistsError
from datetime import datetime, timedelta, timezone
import os
from app.core.config import settings

connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
container_name = settings.AZURE_STORAGE_CONTAINER_NAME
account_name = settings.AZURE_STORAGE_ACCOUNT_NAME
account_key = settings.AZURE_STORAGE_ACCOUNT_KEY


blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def upload_file_to_blob(file_name: str, file_content: bytes, content_type: str) -> str:
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(file_content, content_type=content_type, overwrite=True)
        return blob_client.url
    except ResourceExistsError:
        return blob_client.url

def delete_file_from_blob(file_name: str):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file_name)
        blob_client.delete_blob()
    except Exception as e:
        print(f"Error deleting file: {e}")

async def get_file_url(file_name: str) -> str:
    if not file_name:
        raise ValueError("file_name cannot be None or empty")
    
    try:
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=file_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.now(timezone.utc) + timedelta(hours=1)
        )
        return f"https://{account_name}.blob.core.windows.net/{container_name}/{file_name}?{sas_token}"
    except Exception as e:
        print(f"Error generating file URL: {e}")
        raise