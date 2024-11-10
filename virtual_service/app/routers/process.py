import random
import asyncio

from fastapi import APIRouter, status, Depends

from app.models.request import ProcessRequest
from app.models.response import ProcessResponse
from app.clients.main_api_client import MainApiClient
from app.logging import logging, logger

process_router = APIRouter(tags=["API"])

def get_client() -> MainApiClient:
    return MainApiClient()

def get_random_number() -> float:
    return random.random() * 10

@process_router.post("/process", response_model=ProcessResponse, status_code=status.HTTP_202_ACCEPTED)
async def process_record(request: ProcessRequest, main_api_client: MainApiClient = Depends(get_client)):
    rand = get_random_number() # For testing purposes only
    if rand >=5 :
        # Success
        logger.log(level=logging.INFO, msg=f"Succeded item ({request.__dict__})")
        await asyncio.sleep(5)
        asyncio.create_task(main_api_client.post_process(request.id, True))
        return ProcessResponse(success=True)
  
    # Fail
    logger.log(level=logging.ERROR, msg=f"Failed item ({request.__dict__})")
    await asyncio.sleep(5)
    asyncio.create_task(main_api_client.post_process(request.id, False))
    return ProcessResponse(success=False)
