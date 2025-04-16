"""Response Models for Neoathena API"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FileMetadata(BaseModel):
    """File metadata"""

    user: str | int
    type: str
    size: int


class UploadResponse(BaseModel):
    """Upload to Collection response"""

    status: str
    collection_name: str
    document_id: int
    filename: str
    metadata: FileMetadata


class Document(BaseModel):
    id: Optional[int] = None
    user_id: int
    type: str
    name: str
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()


class Collection(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: str
    created_on: datetime = datetime.now()
    last_updated: datetime = datetime.now()
    documents: list[Document] = []


class GetCollectionsResponse(BaseModel):
    """Get Collections response"""

    collections: list[Collection]
