from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.environments import POSTGRES_CONN

engine = create_engine(
    POSTGRES_CONN,
    connect_args={'client_encoding': 'utf8'}
)

Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()