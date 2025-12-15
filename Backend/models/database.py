from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///users.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)
SessionLocal = async_sessionmaker(autocommit=False, 
                            autoflush=False, 
                            class_=AsyncSession,
                            bind=engine,
                            expire_on_commit=False)

Base = declarative_base(metadata=MetaData())
