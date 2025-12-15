from pydantic import BaseModel
from typing import List

class TopSearchTerm(BaseModel):
    """Represents a single entry for a top searched term."""
    term: str
    count: int

class TopQueriedDocument(BaseModel):
    """Represents a single entry for a top Queried document."""
    document_name: str
    citation_count: int

class AnalyticsDashboard(BaseModel):
    """
    Defines the structure for the analytics dashboard API endpoint.
    """
    top_search_terms: List[TopSearchTerm]
    most_referenced_documents: List[TopQueriedDocument]