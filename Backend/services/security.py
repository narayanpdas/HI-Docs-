from fastapi import Depends, HTTPException,WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import os

from db.users.session import get_db
from crud import user_crud

SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_for_dev")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Decodes the JWT token, validates the user, and returns the user object from the DB.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_ws(websocket: WebSocket, 
                            db: Session = Depends(get_db)):
    """
    WebSocket-specific authentication handler.
    Extracts ?token=<JWT> from URL, validates, and returns user.
    Closes the socket on failure.
    """
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise Exception("Missing authentication token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Exception("Invalid token payload")
        user = user_crud.get_user_by_username(db, username=username)
        if not user:
            raise Exception("User not found")
        return user

    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise Exception("Invalid or expired token")
    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise e