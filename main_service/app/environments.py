import os

from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ENVIRONMENT=os.environ.get("ENVIRONMENT")
DEBUG=os.environ.get("DEBUG")
LOG_LEVEL=os.environ.get("LOG_LEVEL")
API_TITLE=os.environ.get("API_TITLE")
APP_PORT=os.environ.get("APP_PORT")

VIRTUAL_API_URL=os.environ.get("VIRTUAL_API_URL")
POSTGRES_CONN=os.environ.get("POSTGRES_CONN")

LOGSTASH_URL=os.environ.get("LOGSTASH_URL")
LOGSTASH_PORT=os.environ.get("LOGSTASH_PORT")