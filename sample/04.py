import logging
from logging.handlers import HTTPHandler
http_handler = HTTPHandler('www.example.com', '/log', method='POST')
logger.addHandler(http_handler)
