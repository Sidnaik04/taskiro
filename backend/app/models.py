from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import expression
import uuid
from .database import Base

try:
    from sqlalchemy.dialects.sqlite import BLOB as SQLITE_UUID
except Exception:
    SQLITE_UUID = String


class Task(Base):
    __tablename__ = "tasks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), index=True, nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=False)
    image_url = Column(String(600), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
