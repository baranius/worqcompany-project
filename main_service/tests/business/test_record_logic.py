import pytest
import uuid

from unittest.mock import MagicMock, AsyncMock, patch

from app.business.record_logic import RecordLogic, RecordStatus, RecordData, VirtualApiClient
from app.database.entities import Record
from app.models.requests import RecordProcessRequest, RecordRequest
from app.models.response import RecordProcessResponse, RecordResponse


@pytest.fixture
def mock_record_data():
    with patch("app.business.record_logic.RecordData") as MockData:
        yield MockData.return_value
    
@pytest.fixture
def mock_virtual_api():
    with patch("app.business.record_logic.VirtualApiClient") as MockClient:
        yield MockClient.return_value

@pytest.fixture
def mock_record_logic(mock_record_data, mock_virtual_api):
    return RecordLogic(
        record_data=mock_record_data,
        virtual_api=mock_virtual_api
    )


@pytest.mark.asyncio
async def test_create_success(mock_record_logic, mock_record_data, mock_virtual_api):
    request = RecordRequest(name="test", description="description")

    mock_record_data.save = MagicMock()
    mock_record_data.save.side_effect=Exception("hello")
    mock_virtual_api.post_process = MagicMock()

    response = await mock_record_logic.create(request)

    assert isinstance(response, RecordResponse)
    assert response.id is not None
    assert response.created_at is not None

'''
@pytest.mark.asyncio
async def test_update_status_processed(record_logic):
    request = RecordProcessRequest(id=str(uuid.uuid4()), success=True)

    record = Record()
    record.status = RecordStatus.CREATED
    record_logic.record_data.get.return_value = record
    record_logic.record_data.save.return_value = record

    response = await record_logic.update_status(request)

    assert isinstance(response, RecordProcessResponse)
    assert response.success is not True
    assert record.status == RecordStatus.PROCESSED
'''