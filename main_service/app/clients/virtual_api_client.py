import httpx
import uuid

from app.logging import logging, logger

from app.environments import VIRTUAL_API_URL

class VirtualApiClient:
    async def post_process(self, record_id: uuid):
        path = f"{VIRTUAL_API_URL}/process"
        logger.log(level=logging.INFO, msg=path)
        body = { "id": str(record_id) }
        async with httpx.AsyncClient() as client:
            response = await client.post(path, json=body)
            if response.status_code >= 300:
                raise Exception(f"SAGA Failed with status code ({response.status_code})")
