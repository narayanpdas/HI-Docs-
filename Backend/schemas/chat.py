from pydantic import BaseModel
from typing import Dict,Any,List,Optional


class LLMResponse(BaseModel):
    """
        Represents a the expected output Structure from the LLM
    """
    context_answer: str
    summary: str
    citation: str

class ChatResponse(BaseModel):
    """
        Docstring for a ChatResponse .
    """
    chat_id:int
    user_query:str
    llm_response:List[LLMResponse]


class ChatRequest(BaseModel):
    """
        Schema for any ChatRequests
    """
    query: str
    top_n: Optional[int] = 3
    filters: Optional[List[str]] = {}
    api_key:Optional[str]

class ChatHistoryItem(BaseModel):
    id:int
    query:str
    response:Dict[str,Any]
    class config:
        from_attribute:True
class ChatHistoryResponse(BaseModel):
    history:List[ChatHistoryItem]

