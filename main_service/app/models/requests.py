from pydantic import BaseModel, Field, UUID4, StrictBool

class RecordRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=5)

class RecordProcessRequest(BaseModel):
    id: UUID4 = Field(UUID4)
    success: bool = Field(StrictBool)