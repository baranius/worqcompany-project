import pytest
import uuid

from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch

from app.business.record_logic import RecordLogic, RecordStatus
from app.database.entities import Record
from app.models.requests import RecordProcessRequest, RecordRequest
from app.models.response import RecordProcessResponse, RecordResponse


@pytest.fixture()
def mock_logic():
    with patch("app.business.record_logic.inject") as mock_inject:
        mock_inject.dependency_overrides_provider = None
        yield RecordLogic()

@pytest.mark.asyncio
async def test_create_success(mock_logic):
    request = RecordRequest(name="test", description="description")
    record = Record()
    record.id = uuid.uuid4()
    record.created_at = datetime.now()

    mock_logic.record_data.save = MagicMock()
    mock_logic.record_data.save.return_value = record
    mock_logic.virtual_api.post_process = AsyncMock()

    response = await mock_logic.create(request)
    assert isinstance(response, RecordResponse)
    assert response.id is not None
    assert response.created_at is not None
    mock_logic.record_data.save.assert_called_once()
    mock_logic.virtual_api.post_process.assert_called_once()


@pytest.mark.asyncio
async def test_update_status_processed(mock_logic):
    request = RecordProcessRequest(id=str(uuid.uuid4()), success=True)

    record = Record()
    record.status = RecordStatus.CREATED
    mock_logic.record_data.get = MagicMock()
    mock_logic.record_data.get.return_value = record
    mock_logic.record_data.save = MagicMock()
    mock_logic.record_data.save.return_value = record

    response = await mock_logic.update_status(request)

    assert isinstance(response, RecordProcessResponse)
    assert response.success is True
    assert record.status == RecordStatus.PROCESSED
    mock_logic.record_data.get.assert_called_once()
    mock_logic.record_data.save.assert_called_once()

@pytest.mark.asyncio
async def test_update_status_failed(mock_logic):
    request = RecordProcessRequest(id=str(uuid.uuid4()), success=False)

    record = Record()
    record.status = RecordStatus.CREATED
    mock_logic.record_data.get = MagicMock()
    mock_logic.record_data.get.return_value = record
    mock_logic.record_data.save = MagicMock()
    mock_logic.record_data.save.return_value = record

    response = await mock_logic.update_status(request)

    assert isinstance(response, RecordProcessResponse)
    assert response.success is True
    assert record.status == RecordStatus.FAILED
    mock_logic.record_data.get.assert_called_once()
    mock_logic.record_data.save.assert_called_once()