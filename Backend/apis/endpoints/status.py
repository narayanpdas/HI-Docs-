from fastapi import APIRouter,Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.users.session import get_db
from sqlalchemy import select
from models.guys import Guys
from typing import Annotated
from starlette.requests import HTTPConnection
from services.redis_service import RedisServer
def get_redis_service(connection:HTTPConnection)->RedisServer:
    return connection.app.state.redis_service


router = APIRouter()

@router.get('/status')
async def status(
    user_token:Annotated[str,Query(description="The FingerPrintjs Id of the user.")],
    db:AsyncSession = Depends(get_db),
    redis_server:RedisServer=Depends(get_redis_service)
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
        return{
            "status":"success",
            "message":f"{redis_server.get(key=user_token)}"
        }
    except Exception as e:
        print(f"Mission Failed, here is the Error as to why\n {e}")
        return{
            "status":"Failed",
            "message":f"Mission Failed, here is the Error as to why\n {e}"
        }



