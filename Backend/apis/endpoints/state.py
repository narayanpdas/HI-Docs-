from fastapi import APIRouter,Request,Depends
from db.users.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.guys import Guys
from pydantic import BaseModel
from typing import Optional
import os,json
router = APIRouter()

class Token(BaseModel):
        token:str
        api_key:Optional[str]=None
        
@router.post('/create')
async def create(
        token:Token,
        db:AsyncSession=Depends(get_db)
        ):
        try:    
                # req = await token
                user_token = token.token
                api_key = token.api_key
                # print(f"User Token: {user_token}\n APIKEY: {api_key}\n")
                stmt = select(Guys).where(Guys.id==user_token)
                user = await db.scalar(stmt)
                if user is not None:
                        user.api_key = api_key
                else:
                        new_guy = Guys(
                                id=user_token, 
                                api_key=api_key,
                                current_process_doc_id=None
                                )
                        db.add(new_guy)
                        print(f"Added {new_guy}")
                await db.commit()
                return {"status":"Success","code":"{user_token}"}
        except Exception as e:
                print(e)
                return {"status":"Failed","code":f"404 with \n{e}"}