from pydantic import BaseModel
from typing import List,Optional

class DocumentMetadata(BaseModel):
    """
    Represents the metadata for a single document stored in the system.
    Useful for an API endpoint that lists all available documents.
    """
    source_document: str
    publication_date: str
    document_type: str

class UploadResponse(BaseModel):
    """
    Defines the response structure for a successful file upload.
    """
    filename: str
    chunks_ingested: int
    message: str = "Document successfully ingested."

class Docs(BaseModel):
    """
    Defines a document's Info Sent to the Frontend.
    """
    id: int
    name: str
    path:Optional[str]=None
    user_token:str
    
class UserDocs(BaseModel):
    id:int
    filename:str
    user_id:str