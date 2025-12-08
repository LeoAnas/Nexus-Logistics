from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from src.domain.schemas import UserCreate, UserRead
from src.domain.security import hash
from src.infrastracture.db.sql.models import User
from src.infrastracture.logging import logger
from src.infrastracture.repositories.base import SQLAlchemyRepository


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = SQLAlchemyRepository[User](session, User)

    async def create_user(self, data: UserCreate) -> UserRead:
        new_user = User(
            email=data.email,
            hashed_password=hash(data.password),
            full_name=data.full_name,
            tenant_id=data.tenant_id,
        )
        try:
            created_user = await self.repository.add(new_user)
            await self.session.commit()
            logger.info(f"Created User With Email Of {data.email}")
            return UserRead.model_validate(created_user)
        except IntegrityError as e:
            await self.session.rollback()
            if "foreign key" in str(e.orig).lower():
                logger.info(
                f"Tenant Does Not Exist, {e}"
            )
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tenant Does Not Exist"
            )
            else:    
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=f"Email Already Exists"
                )

        except Exception as e:
            await self.session.rollback()
            logger.info(f"Couldn't Create User With Email Of {data.email}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="HTTP_500_INTERNAL_SERVER_ERROR",
            )

    async def get_user(self, user_id: UUID) -> UserRead:
        existed_user = await self.repository.get_by_id(user_id)
        if not existed_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
            )
        logger.info(f"Getting User With id Of {user_id}")
        return UserRead.model_validate(existed_user)
