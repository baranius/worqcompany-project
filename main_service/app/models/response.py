import datetime
from pydantic import BaseModel, UUID4


class GlobalErrorResponse(BaseModel):
    error_message: str

class RecordResponse(BaseModel):
    id: UUID4 | None = None
    created_at: datetime.datetime

class RecordProcessResponse(BaseModel):
    success: bool