from sqlalchemy import func,String,Boolean,ForeignKey
from sqlalchemy.orm import mapped_column,Mapped,relationship
from src.infrastracture.db.sql.base import Base,TimestampMixin,SoftDeleteMixin,UUIDMixin
import uuid



# 1. Tenant (The Organization)
class Tenant(Base,UUIDMixin,SoftDeleteMixin,TimestampMixin):
    __tablename__="tenants"
    
    name:Mapped[str]=mapped_column(
        String(length=50),
        nullable=False,
        unique=True
    )
    slug:Mapped[str]=mapped_column(
        String(length=50),
        nullable=False,
        unique=True,
        index=True #indexing the slug because it will be used in the urls and its more safe
    )
    #Relation Ships(we relationship by class_name)back_populates(the column in the other class)
    users=relationship("User",back_populates="tenant",cascade="all, delete-orphan")
    devices=relationship("Device",back_populates="tenant",cascade="all, delete-orphan")
    
# 2. User (The Staff)
class User(Base,UUIDMixin,TimestampMixin,SoftDeleteMixin):
    __tablename__="users"
    
    email:Mapped[str]=mapped_column(
        String(length=255),
        nullable=False,
        index=True,
        unique=True
    )
    hashed_password:Mapped[str]=mapped_column(
        String(length=255),
        nullable=False,
    )
    full_name:Mapped[str]=mapped_column(
        String(length=250),
        nullable=True,
    )
    is_active:Mapped[bool]=mapped_column(
        Boolean,
        default=True
    )
    is_superuser:Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )
    #Foriegn Keys
    tenant_id:Mapped[uuid.UUID]=mapped_column( # foriegnkeys are added by  tablename.column
        ForeignKey("tenants.id"),
        nullable=False
    )
    tenant=relationship("Tenant",back_populates="users")
    
# 3. Device (The Hardware)
class Device(UUIDMixin,Base,SoftDeleteMixin,TimestampMixin):
    __tablename__="devices"
    
    name:Mapped[str]=mapped_column(
        String(length=50),
        nullable=False,
    )
    device_key:Mapped[str]=mapped_column(
        String(length=50),
        nullable=False,
        index=True,
        unique=True,
    )
    is_online:Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )
    tenat_id:Mapped[uuid.UUID]=mapped_column(
        ForeignKey("tenants.id"),
        nullable=False
    )
    tenant=relationship("Tenant",back_populates="devices")
    
    
