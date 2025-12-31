from fastapi import APIRouter, Depends,WebSocket,WebSocketDisconnect,Query
from starlette.requests import HTTPConnection

from services.rag_service import RAGService
from services.redis_service import RedisManager

from schemas.chat import ChatRequest

from models.docs import Documents
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.users.session import get_db

from typing import Annotated

import json,traceback

router = APIRouter()
CHAT_CREDIT_COST = 20

def get_rag_service(connection:HTTPConnection)->RAGService:
    return connection.app.state.rag_service

def get_redis_service(connection:HTTPConnection)->RedisManager:
    return connection.app.state.redis_service

@router.websocket("/ws/chat")
async def handle_chat_query(
    websocket:WebSocket,
    token:Annotated[str|None, Query()]=None,
    rag_service:RAGService=Depends(get_rag_service),
    redis_server:RedisManager=Depends(get_redis_service),
    db:AsyncSession=Depends(get_db)
):
    await websocket.accept()
    try:
        print("Authenticated...") 
        await websocket.send_json({"type": "auth_status", 
            "message": "Authenticated and ready."})
        while True:
                
                print(f"\n Token: {token} \n")
                data = await websocket.receive_text()
                payload = json.loads(data)
                query = payload.get("query")
                top_n = payload.get("top_n")
                filter_ids = payload.get("filters")
                api_key = payload.get("api_key")
                credits = redis_server.check_credits(user_id=token)
                # TODO Adjust Crediting System.
                if int(credits) < CHAT_CREDIT_COST:
                    await websocket.send_json({"type":"llm",
                                               "value":f"Current Credits: {credits}, Cannot Complete Request"
                                            })
                    await websocket.close()
                    return None
                if len(filter_ids['doc_ids'])!=0: 
                    filter_ids = [int(s) for s in filter_ids['doc_ids']]
                    stmt = select(Documents).filter(Documents.id.in_(filter_ids))
                    filter_docs = await db.scalars(stmt)
                    print(filter_docs)
                    filter_names = [doc.name for doc in filter_docs]
                    await websocket.send_json({"type":"status" ,
                                            "message": f"Processing Recieved {query}"})     
                    collected_data = {}
                    redis_server.decr_credits(user_id=token,
                                              amnt=CHAT_CREDIT_COST)
                    async for model_state in rag_service.get_compliance_answer(ChatRequest(query=query,
                                                                                        top_n=top_n,
                                                                                        filters=filter_names,
                                                                                        api_key=api_key if api_key else "")):
                        collected_data.update(model_state)
                        await websocket.send_json(model_state)    
                    await websocket.send_json({"type": "final", "data": "Finished Processing"})
                else: 
                    await websocket.send_json({"type": "nofiles", "data": "No Files Selected To Search."})
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        traceback.print_exc()
        print("Error: ",e)
        await websocket.send_json({"type":"error","message":str(e)})
        await websocket.close()


        
        