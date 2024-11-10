import uuid

from app.logging import logging, logger
from app.database.entities import Record
from app.database.infra import Session

class RecordData:
    def __init__(self) -> None:
        self.session = Session()

    def save(self, entity: Record) -> Record:
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as exception:
            logger.log(logging.ERROR, f"Save record failed due to: {exception}")

    def get(self, id: uuid) -> Record:
        try:
            entity = self.session.query(Record).get(id)
            return entity
        except Exception as exception:
            logger.log(logging.ERROR, f"Get record failed due to: {exception}")