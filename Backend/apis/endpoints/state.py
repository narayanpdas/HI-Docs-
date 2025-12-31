from fastapi import APIRouter,Depends
from starlette.requests import HTTPConnection
from db.users.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.guys import Guys
from pydantic import BaseModel
from typing import Optional
from services.redis_service import RedisManager
# import os,json


def get_redis_service(connection:HTTPConnection)->RedisManager:
        return connection.app.state.redis_service

router = APIRouter()

class Token(BaseModel):
        token:str
        api_key:Optional[str]=None
        
@router.post('/create')
async def create(
        token:Token,
        db:AsyncSession=Depends(get_db),
        redis_server:RedisManager=Depends(get_redis_service)
        ):
        try:    

                user_token = token.token
                api_key = token.api_key
                stmt = select(Guys).where(Guys.id==user_token)
                user = await db.scalar(stmt)
                free_tokens=100 # TODO: Changes required accordingly.
                if user is not None:
                        user.api_key = api_key
                else:
                        new_guy = Guys(
                                        id=user_token, 
                                        api_key=api_key,
                                        free_credits = free_tokens, 
                                        current_process_doc_id=None
                                )
                        db.add(new_guy)
                        redis_server.add(prefix=redis_server.setname_creditcount,
                                        key=user_token,
                                        value=free_tokens,
                                )
                        print(f"Added {new_guy}")
                await db.commit()
                return {"status":"Success","code":"{user_token}"}
        except Exception as e:
                print(e)
                return {"status":"Failed","code":f"404 with \n{e}"}