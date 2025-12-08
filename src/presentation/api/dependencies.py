from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastracture.db.sql.session import get_db
from src.application.services.tenant_service import TenantService
from src.application.services.user_service import UserService


async def get_tenant_service(session: AsyncSession = Depends(get_db)):
    return TenantService(session)


async def get_user_service(session: AsyncSession = Depends(get_db)):
    return UserService(session)
