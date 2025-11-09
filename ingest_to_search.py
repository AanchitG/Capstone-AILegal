import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

blob_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=AzureKeyCredential(search_api_key))

def ingest_blobs_to_search(container_name):
    container_client = blob_service_client.get_container_client(container_name)
    blobs = container_client.list_blobs()

    documents = []
    for blob in blobs:
        blob_data = container_client.download_blob(blob.name).readall().decode("utf-8")
        documents.append({"id": blob.name, "content": blob_data})

    if documents:
        result = search_client.upload_documents(documents)
        print(f"Uploaded {len(documents)} documents to index '{index_name}'.")
    else:
        print("No documents found to ingest.")

if __name__ == "__main__":
    ingest_blobs_to_search("your-container-name")
