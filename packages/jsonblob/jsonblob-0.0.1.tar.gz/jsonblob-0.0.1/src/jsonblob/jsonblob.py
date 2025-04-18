import requests
from urllib.parse import urlparse
import json

import logging

logger = logging.getLogger(__name__)


class JSONBlobClient:
    # Blob is removed after 30 days of inactivity
    # Approximately
    CONTENT_LENGTH_LIMIT = 1500503  # response.headers.get("Content-Length")

    def __init__(self):
        self.api_url = "https://jsonblob.com/api/jsonBlob"

    def create(self, data: dict) -> str:
        try:
            response = requests.post(self.api_url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

            if not response.ok:
                logger.error(response.status_code)
                return None

            location = response.headers.get("Location")
            blob_id = urlparse(location).path.split("/")[-1]
            return blob_id
        except Exception as error:
            logger.error(error)
            return None

    def update(self, blob_id: str, data: dict) -> bool:
        try:
            response = requests.put(
                f"{self.api_url}/{blob_id}", headers={"Content-Type": "application/json"}, data=json.dumps(data)
            )

            if not response.ok:
                logger.error(response.status_code)
                return False

            return True
        except Exception as error:
            logger.error(error)
            return False

    def get(self, blob_id: str) -> dict:
        try:
            response = requests.get(f"{self.api_url}/{blob_id}")

            if not response.ok:
                logger.error(response.status_code)
                return None

            data = response.json()
            return data
        except Exception as error:
            logger.error(error)
            return None


class JSONBlobStorage:

    def __init__(self, keys_blob_id: str = None):
        self.json_blob_client = JSONBlobClient()
        self.keys = {}
        self.keys_blob_id = keys_blob_id

        if self.keys_blob_id:
            keys = self.json_blob_client.get(self.keys_blob_id)
            if keys == None:
                self.keys_blob_id = self.json_blob_client.create({})
                if not self.keys_blob_id:
                    raise Exception(f"Missing keys_blob_id")
            else:
                self.keys = keys
        else:
            self.keys_blob_id = self.json_blob_client.create({})
            if not self.keys_blob_id:
                raise Exception(f"Missing keys_blob_id")

    def set(self, key: str, value: dict) -> bool:
        blob_id = self.keys.get(key)
        if blob_id:
            return self.json_blob_client.update(blob_id, value)
        else:
            blob_id = self.json_blob_client.create(value)
            if blob_id:
                self.keys[key] = blob_id
                return self.json_blob_client.update(self.keys_blob_id, self.keys)
        return False

    def get(self, key: str) -> dict:
        blob_id = self.keys.get(key)

        if not blob_id:
            return None

        return self.json_blob_client.get(blob_id)
