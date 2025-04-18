# jsonblob

Non official jsonblob api client

## API

<https://jsonblob.com/api>

## Usage

```python
from jsonblob import JSONBlobClient

json_blob = JSONBlobClient()

blob_id = json_blob.create({"hello": "world"})
success = json_blob.update({"zebra": "bebra"})

print(json_blob.get(blob_id))

```

```python
from jsonblob import JSONBlobStorage

json_blob = JSONBlobStorage(keys_blob_id = None)

print(json_blob.keys_blob_id)
print(json_blob.keys)

blob_id = json_blob.set("Zebra", {"hello": "world"})

print(json_blob.get("Zebra"))

```
