import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))
from src.jsonblob import JSONBlobClient, JSONBlobStorage


def test():
    keys_blob_id = "1362505526906380288"
    json_storage = JSONBlobStorage(keys_blob_id)
    print(json_storage.keys_blob_id)
    # json_storage.set("zebra", {"hello": "world"})
    print(json_storage.get("zebra"))


if __name__ == "__main__":
    test()
