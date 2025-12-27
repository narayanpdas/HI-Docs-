from fastapi import UploadFile,APIRouter,status,BackgroundTasks,Request
from fastapi import Query,Depends,File
from starlette.requests import HTTPConnection

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,and_
from db.users.session import get_db
from models.docs import Documents
from models.docs import UserDocuments
from models.guys import Guys

from services.rag_service import RAGService
from starlette.requests import HTTPConnection
from services.redis_service import RedisServer
from redis import Redis


from schemas.upload import UploadResponse
from typing import Annotated

from pathlib import Path
import aiofiles
import uuid
import os
import hashlib


async def calculate_file_hash(file_path:str,file:UploadFile)->str:
    sha256_hash = hashlib.sha256()
    async with aiofiles.open(file_path,'wb') as file_:
        while chunk := await file.read(1024 * 1024): 
            sha256_hash.update(chunk)
            await file_.write(chunk)
    return sha256_hash.hexdigest()


def get_rag_service(connection:HTTPConnection)->RAGService:
    return connection.app.state.rag_service

def get_redis_service(connection:HTTPConnection)->Redis:
    return connection.app.state.redis_service

async def process_pdf(rag_service:RAGService,user_id:str,doc_id:int):
    await rag_service.process_pdf(user_id=user_id,
                                doc_id=doc_id)

router = APIRouter()



@router.post('/upload',
            response_model=UploadResponse,
            status_code=status.HTTP_202_ACCEPTED)
async def upload(
    user_token:Annotated[str,Query(description='Unique FingerPrintJs key of the User.')],
    file:Annotated[UploadFile,File(description="A Pdf File")],
    background:BackgroundTasks,
    rag_service:RAGService=Depends(get_rag_service),
    redis_server:Redis=Depends(get_redis_service),
    db:AsyncSession = Depends(get_db),
):
    if file.content_type != "application/pdf":
        return{
            "status":"failed",
            "message":"Please Upload Pdf Files only"
        }
    save_path = Path.cwd() / "files"
    save_path.mkdir(exist_ok=True)
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    temp_file = save_path / unique_filename
    try:        
        file_hash = await calculate_file_hash(file_path=temp_file,file=file)
        stmt = select(Documents).where(Documents.hash==file_hash)
        file_ = await db.scalar(stmt)
        if file_:
            os.remove(temp_file)
            stmt = select(UserDocuments).where(
                and_(
                    UserDocuments.user_id==user_token,
                    UserDocuments.file_id==file_hash
                )
            )
            check_dup = await db.scalar(stmt)
            if check_dup:
                return{
                    "status":"failed",
                    "message":f"\n Duplicate Files."
                }
            doc_link = UserDocuments(user_id=user_token,
                                    file_id=file_hash,
                                    filename=file.filename
            )
            db.add(doc_link)
            await db.commit()
        else:
            doc = Documents(
                            name = unique_filename,
                            path = str(temp_file),
                            hash = file_hash,
                            is_processed=False
                )
            doc_link = UserDocuments(
                                user_id=user_token,
                                file_id=file_hash,
                                filename=file.filename
                )
            db.add(doc_link)
            db.add(doc)
            await db.flush()
            user = await db.scalar(select(Guys).where(Guys.id == user_token))
            user.current_process_doc_id = doc.id
            redis_server.set(name=user_token,value=doc.id)
            background.add_task(process_pdf,
                                rag_service=rag_service,
                                doc_id=doc.id,
                                user_id=user_token
                                )
            
            print(f"Added {file.filename} to {save_path}...")
        await db.commit()
    except Exception as e:
        return {
            "status":"failed",
            "message":f"\n The Following Error Occurred: \n{e}"
        }
    finally:
        file.file.close()
    return {
        "status":"success",
        "message":"File Uploaded Successfully."
    }









