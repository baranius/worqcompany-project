import uuid

from sqlalchemy import Column, String, Nullable, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.database.infra import Base, engine

class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Nullable(Column(String))
    description = Nullable(Column(String))
    created_at = Nullable(Column(DateTime))
    status = Nullable(Column(String))

Base.metadata.create_all(engine)