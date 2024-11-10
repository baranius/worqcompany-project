from pydantic import BaseModel, UUID4


class ProcessRequest(BaseModel):
    id: UUID4

