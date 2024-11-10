from pydantic import BaseModel


class ProcessResponse(BaseModel):
    success: bool

