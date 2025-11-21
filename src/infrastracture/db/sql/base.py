import uuid
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from datetime import datetime
from sqlalchemy import func,UUID,DateTime,BOOLEAN

class Base(DeclarativeBase):
    """
    BASE class for all sql_alchemy models 

    Args:
        DeclarativeBase (_type_): _description_
    """
    pass



class UUIDMixin:
    """
    Mixin to provide uuid for all models
    """
    id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True), #so python will read it as uuid objects not strings
        primary_key=True,    #to make it primary key
        default=uuid.uuid4, #default value if no id is provided
        index=True          # for performance optimization
    )
    

class TimestampMixin:
    """
    Mixin to provide created_at and updated_at columns for all models
    """
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(), # server default is on db side --- default is python side,
        nullable=False
    )
    updated_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(), #automatically update that column value on update that happens to the relevant rows
        nullable=False 
    )


class SoftDeleteMixin:
    """
    Never actually delete data just hide it 
    Essential for Auditing and recovery
    """
    is_deleted:Mapped[bool]=mapped_column(
        BOOLEAN,
        default=False,
        index=True
    )
    deleted_at:Mapped[datetime|None]=mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    