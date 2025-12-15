from fastapi import APIRouter,Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.users.session import get_db
from sqlalchemy import select
from models.guys import Guys
from typing import Annotated



router = APIRouter()

@router.get('/status')
async def status(
    user_token:Annotated[str,Query(description="The FingerPrintjs Id of the user.")],
    db:AsyncSession = Depends(get_db)
):
    # TODO: Update this to SSE version, i.e. Server Sent Event
    """
    Status Endpoint, Provides status of the User's File request, whether its still processing or has
    been already processed.

    Args:
        user_token (Annotated[str,Query, optional): _description_. Defaults to "The FingerPrintjs Id of the user.")].
        db (AsyncSession, optional): _description_. Defaults to Depends(get_db).
    """
    try:
        get_current_user = select(Guys).where(Guys.id==user_token)
        res = await db.execute(get_current_user)
        user_status = res.scalar().current_process_doc_id
        return{
            "status":"success",
            "message":f"{user_status}"
        }
    except Exception as e:
        print(f"Mission Failed, here is the Error as to why\n {e}")
        return{
            "status":"Failed",
            "message":f"Mission Failed, here is the Error as to why\n {e}"
        }



