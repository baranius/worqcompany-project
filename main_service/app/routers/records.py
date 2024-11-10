from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.business.record_logic import RecordLogic
from app.models.requests import RecordRequest, RecordProcessRequest
from app.models.response import RecordResponse, RecordProcessResponse, GlobalErrorResponse

record_router = APIRouter(tags=["API"])

def get_logic() -> RecordLogic:
    return RecordLogic()

@record_router.post("/record", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
async def save_record(request: RecordRequest, record_logic: RecordLogic = Depends(get_logic)):
    try:
        response = await record_logic.create(request)
        return response
    except Exception as exception:
        response = GlobalErrorResponse(error_message=str(exception))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.__dict__)
    
@record_router.post("/record/status", response_model=RecordProcessResponse, status_code=status.HTTP_200_OK)
async def update_process(request: RecordProcessRequest, record_logic: RecordLogic = Depends(get_logic)):
    try:
        response = await record_logic.update_status(request)
        return response
    except Exception as exception:
        response = GlobalErrorResponse(error_message=str(exception))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.__dict__)