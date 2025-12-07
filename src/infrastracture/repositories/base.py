from typing import Generic, TypeVar, List, Optional, Type
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.application.interfaces.repository import IRepository
from src.infrastracture.db.sql.base import Base, UUIDMixin, SoftDeleteMixin
from src.infrastracture.db.sql.models import MappedModel


# A class so it help with type checking and py autocompletion for objects eg self.model.->(the object itself)

ModelType = TypeVar("ModelType", bound=MappedModel)
# ModelType = TypeVar("ModelType")


class SQLAlchemyRepository(IRepository[ModelType], Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, uuid: UUID) -> Optional[ModelType]:
        stmt = select(self.model).where(
            self.model.id == uuid, self.model.deleted_at == False
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # we dont commit here its service responsiblity (Unit Of Work)
    # we flushed so we can get the generated id
    # we refreshed so we can get the server default columns that come from DB
    async def add(self, entity: ModelType) -> ModelType:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    # list in the return because scalars.all returns a sequence not a list so we cast it to avoid type error
    async def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = (
            select(self.model)
            .where(self.model.deleted_at == False)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
