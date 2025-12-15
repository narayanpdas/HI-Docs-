from fastapi import APIRouter, Depends,Query,status
from db.users.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from typing import Annotated
from models.docs import UserDocuments
from schemas.document import Docs,UserDocs
import asyncio

# from fastapi.security import OAuth2PasswordBearer
# SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_for_dev")
# ALGORITHM = "HS256"
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")



router = APIRouter()
@router.get('/docs',
            response_model=List[UserDocs],
            status_code=status.HTTP_200_OK)
async def get_docs(
    user_token:Annotated[str,Query(description="User's Unqiue Id with FingerPrintJS.")],
    db:AsyncSession = Depends(get_db),
    ):
    print("Called For Docs by",user_token)
    stmt = select(UserDocuments).where(UserDocuments.user_id == user_token)
    all_docs = await db.execute(stmt) # For getting all the Docs of the user's...
    if all_docs:
        all_docs = all_docs.scalars().all()
        await asyncio.sleep(1)
        return all_docs
    return []
    