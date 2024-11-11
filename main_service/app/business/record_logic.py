import asyncio
from datetime import datetime
from fast_depends import Depends, inject

from app.database.entities import Record
from app.database.records_data import RecordData
from app.clients.virtual_api_client import VirtualApiClient
from app.models.requests import RecordRequest, RecordProcessRequest
from app.models.response import RecordResponse, RecordProcessResponse

class RecordStatus:
    CREATED = "CREATED"
    FAILED = "FAILED"
    PROCESSED = "PROCESSED"

class RecordLogic:
    @inject
    def __init__(
            self, 
            record_data: RecordData = Depends(RecordData), 
            virtual_api: VirtualApiClient = Depends(VirtualApiClient)
        ):
        self.record_data = record_data
        self.virtual_api = virtual_api

    async def create(self, request: RecordRequest) -> RecordResponse:
        entity = Record()
        entity.name = request.name,
        entity.description = request.description,
        entity.created_at = datetime.now(),
        entity.status = RecordStatus.CREATED,
        entity = self.record_data.save(entity)

        asyncio.create_task(self.virtual_api.post_process(entity.id))

        response = RecordResponse(
            id=str(entity.id),
            created_at=str(entity.created_at)
        )
        return response
    
    async def update_status(self, request: RecordProcessRequest) -> RecordProcessResponse:
        entity = self.record_data.get(request.id)
        if request.success:
            entity.status = RecordStatus.PROCESSED
        else:
            entity.status = RecordStatus.FAILED
        self.record_data.save(entity)
        return RecordProcessResponse(success=True)
        
