from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastracture.db.sql.session import get_db
from src.application.services.tenant_service import TenantService

async def get_tenant_service(session:AsyncSession=Depends(TenantService)):
    return TenantService(session)