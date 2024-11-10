import logging
from logstash import TCPLogstashHandler

from app.environments import API_TITLE, LOGSTASH_URL, LOGSTASH_PORT

# Logging
# Configure logger
logger = logging.getLogger('python-logger')
logger.setLevel(logging.INFO)

# Set up the Logstash handler
logstash_handler = TCPLogstashHandler(host=LOGSTASH_URL, port=LOGSTASH_PORT, tags=API_TITLE, version=1)
logger.addHandler(logstash_handler)