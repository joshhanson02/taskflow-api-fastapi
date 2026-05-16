import logging
import os
from logging.handlers import RotatingFileHandler
from core.config import settings

# Tạo thư mục logs nếu chưa có
if not os.path.exists("logs"):
    os.makedirs("logs")

LOG_FORMAT = (
    "%(asctime)s - "
    "%(name)s - "
    "%(levelname)s - "
    "%(message)s"
)

formatter = logging.Formatter(LOG_FORMAT)

file_handler = RotatingFileHandler(
    filename="logs/app.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)

if settings.ENV == "development":
    log_level = logging.DEBUG

elif settings.ENV == "production":
    log_level = logging.INFO

else:
    log_level = logging.WARNING

logging.basicConfig(
    level=log_level,
    handlers=[
        file_handler,
        console_handler
    ]
)

logger = logging.getLogger(__name__)
