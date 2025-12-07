from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID

from src.domain.schemas import TenantCreate, TenantRead
from src.infrastracture.repositories.base import SQLAlchemyRepository
from src.infrastracture.db.sql.models import Tenant
from src.infrastracture.logging import logger


class TenantService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = SQLAlchemyRepository(session, Tenant)

    async def create_tenant(self, data: TenantCreate) -> TenantRead:
        # 1. Convert DTO to Entity
        new_tenant = Tenant(name=data.name, slug=data.slug)
        try:
            # 2- add to db
            created_tenant = await self.repository.add(new_tenant)
            # 3- commit transaction(service layer responsability)
            await self.session.commit()
            logger.info(f"Tenant Created Successfuly: {created_tenant.id}")
            return TenantRead.model_validate(created_tenant)
        except IntegrityError:
            await self.session.rollback()
            logger.warning(f"Attemped to Create duplicate tenant slug : {data.slug}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tenant with this slug or name already exists.",
            )
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating tenant: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )

    async def get_tenant(self, tenant_id: UUID) -> TenantRead:
        tenant = await self.repository.get_by_id(tenant_id)
        if not tenant:
            logger.error(f"Could Not find a tenant with id of {tenant_id} ")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tenant Not Found"
            )
        return TenantRead.model_validate(tenant)
