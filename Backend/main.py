from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from apis.endpoints import docs
from apis.endpoints import state
from apis.endpoints import upload
from apis.endpoints import chat
from apis.endpoints import status
from services.rag_service import RAGService
from services.redis_service import RedisManager


from db.users.session import create_tables



        
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the application's startup and shutdown events."""
    print("--- Loading Models---")
    await create_tables()
    app.state.rag_service = RAGService()
    app.state.redis_service = RedisManager()

    yield
    print("--- App Shutdown ---")
app = FastAPI(lifespan = lifespan)

# TODO Change required during Deployment.
origins = [
    "http://localhost:5173",   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              
    allow_credentials=True,
    allow_methods=["*"],                
    allow_headers=["*"],               
)


app.include_router(chat.router,prefix="/api/v1",tags=["Chat"])
app.include_router(docs.router,prefix="/api/v1",tags=["Docs"])
app.include_router(state.router,prefix="/api/v1",tags=["Guys"])
app.include_router(upload.router,prefix="/api/v1",tags=["Upload"])
app.include_router(status.router,prefix="/api/v1",tags=["status"])

@app.get('/',tags=['Root'])
def read_root():
    return {"Status":"Main Page Running!"}
