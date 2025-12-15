from models.guys import Guys
# from models.chat import ChatHistory
from models.docs import Documents
from models.database import engine,Base,SessionLocal



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
async def get_db():
    """
        This function is a dependency that creates a new database session for
        each request, and then safely closes it when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
        
def get_func_db():
    return SessionLocal()