from fastapi import APIRouter, Depends, status
from src.application.services.tenant_service import TenantService
from src.domain.schemas import TenantCreate, TenantRead
from src.presentation.api.dependencies import get_tenant_service
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_data: TenantCreate, service: TenantService = Depends(get_tenant_service)
):
    return await service.create_tenant(tenant_data)


@router.get("/{tenant_id}", response_model=TenantRead, status_code=status.HTTP_200_OK)
async def get_tenant(
    tenant_id: UUID, service: TenantService = Depends(get_tenant_service)
):
    return await service.get_tenant(tenant_id)

