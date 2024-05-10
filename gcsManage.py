from google.cloud import storage
import datetime
from google.oauth2 import service_account
import streamlit as st
import json

def upload_csv(local_file_name, destination_blob_name):
    """Uploads a csv to the given Cloud Storage bucket and returns a message."""

    gcp_credentials = json.loads(st.secrets["gcp_service_account"]["key"], strict=False)
    credentials = service_account.Credentials.from_service_account_info(gcp_credentials)

    bucket_name = "misinfo-harm"
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_name)


def generate_signed_url(file_path):

    gcp_credentials = json.loads(st.secrets["gcp_service_account"]["key"], strict=False)
    credentials = service_account.Credentials.from_service_account_info(gcp_credentials)

    bucket_name = "misinfo-harm"
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(file_path)

    if not blob.exists():
        return None
    
    url = blob.generate_signed_url(
        method="GET",
        version="v4",
        expiration= datetime.timedelta(seconds=3600)
    )

    return url