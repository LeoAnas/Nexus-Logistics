from fastapi import Depends, status, APIRouter
from uuid import UUID

from src.domain.schemas import UserCreate, UserRead
from src.presentation.api.dependencies import get_user_service
from src.application.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate, service: UserService = Depends(get_user_service)
):
    return await service.create_user(data)


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    return await service.get_user(user_id)
