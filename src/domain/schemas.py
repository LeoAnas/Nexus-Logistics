from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )  # to allow pydantic model to validate orm object automatically


# tenants schemas
class TenantBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=50)
    slug: str = Field(..., min_length=2, max_length=50, pattern="^[a-z0-9-A-Z]+$")


class TenantCreate(TenantBase):
    pass


class TenantRead(TenantBase):
    id: UUID
    created_at: datetime
    is_active: bool = True


# user schemas
class UserBase(BaseSchema):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50)
    tenant_id: UUID


class UserRead(UserBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime
