from langchain_core.documents import Document as LangChainDocument
from typing import Optional
import mimetypes
import requests
import aiohttp
import os
from .models import UploadResponse, GetCollectionsResponse, Collection


class NeoAthenaClient:
    def __init__(self, api_key: str):
        """Initialize the NeoAthenaClient"""

        self.BASE_URL = "https://neoserverprod.raen.ai"
        self.__API_KEY = api_key or os.getenv("NEOATHENA_API_KEY")
        if not self.__API_KEY:
            raise ValueError(
                "API key not found. Please set it as an environment variable \
                (`NEOATHENA_API_KEY`) or pass it as an argument."
            )

    def get_collections(self) -> GetCollectionsResponse:
        """
        Gets all collections for a user.

        Returns:
            GetCollectionsResponse: A list of collections with their details

        Raises:
            RequestException: If the request fails
        """
        url = f"{self.BASE_URL}/collections/"

        try:
            response = requests.get(
                url,
                headers={
                    "Accept": "application/json",
                    "X-API-Key": self.__API_KEY,
                },
                timeout=30,
            )
            response.raise_for_status()
            json_collections = response.json()
            if isinstance(json_collections, list):
                return GetCollectionsResponse(
                    collections=[
                        Collection(**collection) for collection in json_collections
                    ]
                )
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, "status_code", "N/A")
            print(f"Request failed: {str(e)}")
            print(f"Response status code: {status_code}")
            print(f"Response text: {getattr(e.response, 'text', 'N/A')}")
            raise

    def upload_to_collection(
        self, collection_name: str, filepath: str
    ) -> UploadResponse:
        """
        Upload a file to the collection.

        Args:
            collection_name (str): The name of the collection to upload the file to.
            files (str): The file path to upload.

        Returns:
            UploadResponse: Response from the server

        Raises:
            FileNotFoundError: If the specified file doesn't exist
            ValueError: If the collection name is invalid
            RequestException: If the upload request fails
        """
        if not collection_name:
            raise ValueError("Collection name cannot be None")

        url = f"{self.BASE_URL}/collections/upload/{collection_name}"

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            with open(filepath, "rb") as f:
                filename = os.path.basename(filepath)
                content_type, _ = mimetypes.guess_type(filepath)

                if content_type is None:
                    content_type = "application/octet-stream"

                files_to_upload = {"file": (filename, f, content_type)}

                headers = {
                    "Accept": "application/json",
                    "X-API-Key": self.__API_KEY,
                }
                response = requests.post(
                    url, files=files_to_upload, headers=headers, timeout=30
                )
                response.raise_for_status()

                try:
                    return UploadResponse(**response.json())
                except requests.exceptions.JSONDecodeError:
                    return {"status": response.status_code, "response": response.text}

        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, "status_code", "N/A")
            print(f"Upload failed: {str(e)}")
            print(f"Response status code: {status_code}")
            print(f"Response text: {getattr(e.response, 'text', 'N/A')}")
            raise

    def retrieve_from_collection(
        self,
        query: str,
        collection_name: str,
        file_names: Optional[list[str]] = None,
        top_k: int = 4,
    ) -> list[LangChainDocument]:
        """
        Retrieve documents from the collection based on a search query.

        Args:
            query (str): Search query
            collection_name (str): The name of the collection to search within.
            file_names (Optional[list[str]]): List of file names to retrieve from. If None, retrieves from the entire collection.
            top_k (int): Number of top results to return

        Returns:
            list[Document]: list of relevant documents

        Raises:
            ValueError: If collection_name or query is invalid
            RequestException: If the request fails
        """
        if not collection_name:
            raise ValueError("Collection name cannot be None")
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be a positive integer")

        url = f"{self.BASE_URL}/collections/retrieve/{collection_name}"
        headers = {
            "Accept": "application/json",
            "X-API-Key": self.__API_KEY,
        }
        body = {"query": query, "top_k": top_k}
        if file_names:
            body["file_names"] = file_names

        try:
            response = requests.post(url, headers=headers, json=body, timeout=30)
            response.raise_for_status()

            try:
                json_docs = response.json()
                if isinstance(json_docs, list):
                    docs = []
                    for doc in json_docs:
                        docs.append(LangChainDocument(**doc))
                    return docs
            except requests.exceptions.JSONDecodeError:
                return {"status": response.status_code, "response": response.text}

        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, "status_code", "N/A")
            print(f"Request failed: {str(e)}")
            print(f"Response status code: {status_code}")
            print(f"Response text: {getattr(e.response, 'text', 'N/A')}")
            raise

    async def aretrieve_from_collection(
        self,
        query: str,
        collection_name: str,
        file_names: Optional[list[str]] = None,
        top_k: int = 4,
    ) -> list[LangChainDocument]:
        """
        Asynchronously retrieve documents from the collection based on a search query.

        Args:
            collection_name (str): The name of the collection to search within.
            query (str): Search query
            top_k (int): Number of top results to return

        Returns:
            list[Document]: list of relevant documents

        Raises:
            ValueError: If collection_name or query is invalid
            ClientError: If the request fails
        """
        if not collection_name:
            raise ValueError("Collection name cannot be None")
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be a positive integer")

        url = f"{self.BASE_URL}/collections/retrieve/{collection_name}"
        headers = {
            "Accept": "application/json",
            "X-API-Key": self.__API_KEY,
        }

        body = {"query": query, "top_k": top_k}
        if file_names:
            body["file_names"] = file_names

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json=body,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    await response.raise_for_status()

                    try:
                        json_docs = await response.json()
                        if isinstance(json_docs, list):
                            docs = []
                            for doc in json_docs:
                                docs.append(LangChainDocument(**doc))
                            return docs
                    except aiohttp.ContentTypeError:
                        return {
                            "status": response.status,
                            "response": await response.text(),
                        }

        except aiohttp.ClientError as e:
            status_code = getattr(e, "status", "N/A")
            print(f"Request failed: {str(e)}")
            print(f"Response status code: {status_code}")
            response_text = "N/A"
            if hasattr(e, "message"):
                response_text = e.message
            print(f"Response text: {response_text}")
            raise

    def delete_from_collection(
        self,
        collection_name: str,
        doc_id: Optional[int] = None,
        delete_all: bool = False,
    ) -> bool:
        """
        Delete document(s) from the collection.

        Args:
            collection_name (str): The name of the collection from which to delete documents.
            doc_id (Optional[int]): Document ID to delete. If None, `delete_all` must be True.
            delete_all (bool): Whether to delete all documents. Default is False.

        Returns:
            bool: Deletion confirmation

        Raises:
            ValueError: If collection_name or doc_id is invalid
            RequestException: If the request fails
        """
        if not collection_name:
            raise ValueError("Collection name cannot be None")
        if not isinstance(doc_id, int) and not delete_all:
            raise ValueError("doc_id must be an integer when not deleting all")
        if not isinstance(delete_all, bool):
            raise ValueError("delete_all must be a boolean")

        url = f"{self.BASE_URL}/collections/files/{collection_name}"
        headers = {
            "Accept": "application/json",
            "X-API-Key": self.__API_KEY,
        }
        payload = {"doc_id": doc_id, "delete_all": delete_all}

        try:
            response = requests.delete(url, headers=headers, json=payload, timeout=30)

            response.raise_for_status()
            return True

        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, "status_code", "N/A")
            print(f"Request failed: {str(e)}")
            print(f"Response status code: {status_code}")
            print(f"Response text: {getattr(e.response, 'text', 'N/A')}")
            raise

    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete an entire collection.

        Args:
            collection_name (str): The name of the collection to delete.

        Returns:
            bool: Deletion confirmation

        Raises:
            ValueError: If collection_name is invalid
            RequestException: If the request fails
        """
        if not collection_name:
            raise ValueError("Collection name cannot be None")

        url = f"{self.BASE_URL}/collections/{collection_name}"
        headers = {
            "Accept": "application/json",
            "X-API-Key": self.__API_KEY,
        }
        try:
            response = requests.delete(url, headers=headers, timeout=30)

            response.raise_for_status()
            return True

        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, "status_code", "N/A")
            print(f"Request failed: {str(e)}")
            print(f"Response status code: {status_code}")
            print(f"Response text: {getattr(e.response, 'text', 'N/A')}")
            raise
