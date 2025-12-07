from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine,AsyncSession
from src.config import settings
from typing import AsyncGenerator
#future -> to use sqlalchemy 2.0 style
#pool_pre_ping -> to check if the connection is alive before using it 
async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=settings.ENVIRONMENT == "dev",
    future=True,
    pool_pre_ping=True,
)

#expire_on_commit-> false because by default sqlalchemy will reload the data from the database which will cause more resources
#auto_flush-> False because by default its true ..
# and it means that sql alchemy will automatically sync your upates with the data before making new queries
async_session_local=async_sessionmaker(bind=async_engine,expire_on_commit=False,autoflush=False)

async def get_db()->AsyncGenerator[AsyncSession,None]:
    async with async_session_local() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
        finally:
            await db.close()
            
                
