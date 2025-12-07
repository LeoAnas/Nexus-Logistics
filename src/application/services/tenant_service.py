from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.domain.schemas import TenantCreate, TenantRead
from src.infrastracture.repositories.base import SQLAlchemyRepository
from src.infrastracture.db.sql.models import Tenant
from src.infrastracture.logging import logger


class TenantService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = SQLAlchemyRepository(session, Tenant)
        
    async def create_tenant(self,data:TenantCreate)->TenantRead:
        # 1. Convert DTO to Entity
        new_tenant=Tenant(name=data.name,slug=data.slug)
        try:
            # 2- add to db
            created_tenant=await self.repository.add(new_tenant)
            #3- commit transaction(service layer responsability)
            await self.session.commit()
            logger.info(f"Tenant Created Successfuly: {created_tenant.id}")
            return TenantRead.model_validate
        except:
            pass
            
