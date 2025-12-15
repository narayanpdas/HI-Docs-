from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert,delete


from apis.endpoints import docs
from apis.endpoints import state
from apis.endpoints import upload
from apis.endpoints import chat
from apis.endpoints import status
from services.rag_service import RAGService


from models.docs import Documents
from db.users.session import get_func_db,create_tables
from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path


load_dotenv(find_dotenv('config.env'))
PDF_PATH = os.getenv('PDF_PATH')

# async def _sync_docs_to_folder(db:AsyncSession = get_func_db()):
#         print(f"Searching New Docs in {PDF_PATH}")
#         files_path = Path('files')
        
#         if files_path.is_dir()==False:
#             os.mkdir(path=files_path)
#         else:
#             files_in_disk = set(os.listdir(files_path))
#             stmt = select(Documents.name)
#             files_in_db = set((await db.scalars(stmt)).all())
#             files_to_add = files_in_disk-files_in_db
#             files_to_delete = files_in_db-files_in_disk
#             if files_to_add:
#                 new_docs = [
                    
#                 ]
#             if files_to_delete:
#                 stmt = delete(Documents).where(Documents.name.in_(files_to_delete))
#                 db.execute(stmt)
#         await db.commit()
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the application's startup and shutdown events."""
    print("--- Loading Models---")
    await create_tables()
    app.state.rag_service = RAGService()
    yield
    print("--- App Shutdown ---")
app = FastAPI(lifespan = lifespan)

# TODO Change this during Deployment.
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

# app.include_router(users.router,prefix="/api/v1",tags=["Users"])

app.include_router(chat.router,prefix="/api/v1",tags=["Chat"])
app.include_router(docs.router,prefix="/api/v1",tags=["Docs"])
app.include_router(state.router,prefix="/api/v1",tags=["Guys"])
app.include_router(upload.router,prefix="/api/v1",tags=["Upload"])
app.include_router(status.router,prefix="/api/v1",tags=["status"])

@app.get('/',tags=['Root'])
def read_root():
    return {"Status":"Main Page Running!"}
