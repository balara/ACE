from azure.storage.blob import BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=acestorage123;AccountKey=F8GTinAlI8mnJztwDgnyXEgVqNdJT/2NZeqj/0ZxKOCd2Qncf2F1qltQN91gF0IglicAi8w+MD6b+AStPmA43Q==;EndpointSuffix=core.windows.net")
container_client = blob_service_client.get_container_client("acedata")
blobs = container_client.list_blobs()
print("reading blob...")
for blob in blobs:
    print(blob.name)
    if blob.name.endswith('.pdf'):
        blob_data = container_client.download_blob(blob)
        with open('./'+blob.name, "wb") as my_blob:
            my_blob.write(blob_data.content_as_bytes())
