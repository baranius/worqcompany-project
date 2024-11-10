import pytest
import uuid
from unittest.mock import AsyncMock, patch
from app.clients.main_api_client import MainApiClient
from app.environments import MAIN_API_URL

@pytest.mark.asyncio
async def test_post_process_success():
    record_id = uuid.uuid4()
    success_status = True
    main_api_client = MainApiClient()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200

        await main_api_client.post_process(record_id, success_status)

        mock_post.assert_called_once_with(
            f"{MAIN_API_URL}/record/process",
            json={"id": str(record_id), "success": success_status}
        )

@pytest.mark.asyncio
async def test_post_process_failure():
    record_id = uuid.uuid4()
    success_status = False
    main_api_client = MainApiClient()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 400

        with pytest.raises(Exception) as excinfo:
            await main_api_client.post_process(record_id, success_status)
        
        assert "SAGA Failed with status code (400)" in str(excinfo.value)

        mock_post.assert_called_once_with(
            f"{MAIN_API_URL}/record/process",
            json={"id": str(record_id), "success": success_status}
        )
