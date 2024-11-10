import httpx
import uuid

from app.environments import MAIN_API_URL

class MainApiClient:
    async def post_process(self, record_id: uuid, success: bool):
        path = f"{MAIN_API_URL}/record/status"
        body = { "id": str(record_id), "success": success }
        async with httpx.AsyncClient() as client:
            response = await client.post(path, json=body)
            if response.status_code >= 300:
                raise Exception(f"SAGA Failed with status code ({response.status_code})")
