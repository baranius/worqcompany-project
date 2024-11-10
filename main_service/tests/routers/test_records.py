import pytest
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import status
from fastapi.responses import JSONResponse
from app.main import app
from app.models.requests import RecordRequest, RecordProcessRequest
from app.models.response import RecordResponse, RecordProcessResponse
from app.routers.records import save_record, update_process, get_logic

client = TestClient(app)

@pytest.fixture
def sample_record_request():
    return RecordRequest(name="name", description="description")

@pytest.fixture
def sample_record_process_request():
    return RecordProcessRequest(id=str(uuid.uuid4()), success=True)

@pytest.fixture
def mock_record_logic():
    with patch("app.routers.records.get_logic") as mock_logic:
        yield mock_logic.return_value


# Tests for the /record endpoint
@pytest.mark.asyncio
async def test_save_record_success(sample_record_request, mock_record_logic):
    logic_response = RecordResponse(id=str(uuid.uuid4()), created_at=datetime.now())
    mock_record_logic.create = AsyncMock()
    mock_record_logic.create.return_value = logic_response

    response = await save_record(sample_record_request, mock_record_logic)

    assert response.id == logic_response.id
    assert response.created_at == logic_response.created_at
    mock_record_logic.create.assert_called_once()

@pytest.mark.asyncio
async def test_save_record_failure(sample_record_request, mock_record_logic):
    mock_record_logic.create = AsyncMock()
    mock_record_logic.create.side_effect=Exception("Unexpected error")

    response = await save_record(sample_record_request, mock_record_logic)

    assert isinstance(response, JSONResponse)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.body == b'{"error_message":"Unexpected error"}'
    mock_record_logic.create.assert_called_once()


# Tests for the /record/process endpoint
@pytest.mark.asyncio
async def test_update_process_success(sample_record_process_request, mock_record_logic):
    logic_response = RecordProcessResponse(success=True)
    mock_record_logic.update_status = AsyncMock()
    mock_record_logic.update_status.return_value=logic_response

    response = await update_process(sample_record_process_request, mock_record_logic)

    assert response.success is True
    mock_record_logic.update_status.assert_called_once()

@pytest.mark.asyncio
async def test_update_process_failure(sample_record_process_request, mock_record_logic):
    mock_record_logic.update_status = AsyncMock()
    mock_record_logic.update_status.side_effect=Exception("Process error")

    response = await update_process(sample_record_process_request, mock_record_logic)

    assert isinstance(response, JSONResponse)
    assert response.body == b'{"error_message":"Process error"}'
    mock_record_logic.update_status.assert_called_once()
