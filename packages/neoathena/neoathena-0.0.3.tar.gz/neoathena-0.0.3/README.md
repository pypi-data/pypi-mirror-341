# NeoAthena Python Client

A Python client library for interacting with the NeoAthena API, providing functionality to create and manage collections, upload files, and perform document retrieval operations.

## Installation

```bash
pip install neoathena
```

## Quick Start

```python
from neoathena import NeoAthenaClient

# Initialize the client
client = NeoAthenaClient(api_key="your-api-key")

# Check if the collection exists, create it if it doesn't, and upload the file to the collection
results = client.upload_to_collection(
    collection_name="your-collection-name", 
    filepath="path/to/your/file"
)

# Retrieve documents based on a query
results = client.retrieve_from_collection(
    query="your search query", 
    collection_name="your-collection-name", 
    file_names=["file1.txt", "file2.txt"],
    top_k=4
)

# List your collections
result = client.get_collections()

```

## Features

- Create collection and upload files with automatic content type detection
- Perform semantic search queries
- Delete individual documents or entire collections
- List all user collections
- Built-in error handling and validation

## API Reference

Check out our docs [here](https://docs.neoathena.com).

## Error Handling

The client includes comprehensive error handling for common scenarios:

- `ValueError`: Raised for invalid input parameters
- `FileNotFoundError`: Raised when specified files don't exist
- `requests.exceptions.RequestException`: Raised for network-related errors

Example error handling:

```python
try:
    response = client.upload_to_collection(api_key, "file.pdf")
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Invalid input: {e}")
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
```

## Requirements

- Python 3.8+
- requests library
- Valid API credentials

## License

GNU General Public License v3.0

## Support

For support, please contact support@raen.ai