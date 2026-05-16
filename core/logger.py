import logging
import os

# Tạo thư mục logs nếu chưa có
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",

    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
