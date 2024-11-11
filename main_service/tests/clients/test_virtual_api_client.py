import pytest
import httpx
import uuid

from unittest.mock import AsyncMock, patch

from app.clients.virtual_api_client import VirtualApiClient

@pytest.fixture
def mock_post():
    with patch("httpx.AsyncClient.post") as mock_httpx:
        yield mock_httpx

@pytest.mark.asyncio
async def test_post_process_succeed(mock_post):
    response = httpx.Response(201)
    client = VirtualApiClient()

    mock_post.return_value = response

    await client.post_process(record_id=uuid.uuid4())

@pytest.mark.asyncio
async def test_post_process_failed(mock_post):
    response = httpx.Response(400)

    mock_post.return_value = response

    with pytest.raises(Exception) as exp: 
        await VirtualApiClient().post_process(uuid.uuid4())

    assert f"SAGA Failed with status code ({response.status_code})" == str(exp.value)
