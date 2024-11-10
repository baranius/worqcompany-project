import pytest
import uuid
from unittest.mock import patch, AsyncMock
from app.routers.process import process_record
from app.models.request import ProcessRequest

@pytest.fixture
def sample_request():
    return ProcessRequest(id=str(uuid.uuid4()))

@pytest.fixture
def mock_client():
    with patch("app.routers.process.get_client") as mock_get_client:
        yield mock_get_client.return_value

@pytest.fixture
def mock_random():
    with patch("app.routers.process.get_random_number") as mock_random:
        yield mock_random

@pytest.mark.asyncio
async def test_process_record_success(sample_request, mock_client, mock_random):
    mock_random.return_value = 6

    mock_client.post_process = AsyncMock()

    response = await process_record(sample_request, mock_client)

    assert response.success is True
    mock_client.post_process.assert_called_once_with(sample_request.id, True)

@pytest.mark.asyncio
async def test_process_record_failure(sample_request, mock_client, mock_random):
    mock_random.return_value = 4

    mock_client.post_process = AsyncMock()

    response = await process_record(sample_request, mock_client)

    assert response.success is False
    mock_client.post_process.assert_called_once_with(sample_request.id, False)

