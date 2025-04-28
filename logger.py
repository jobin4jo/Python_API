# logger.py

import logging
import os
from dotenv import load_dotenv

load_dotenv()

app_name = os.getenv("APP_NAME", "myapp")
log_folder = os.getenv("LOG_FILE_PATH", "logs")


log_file_path = os.path.join(log_folder, f"{app_name}.log")

if not os.path.exists(log_folder):
    os.makedirs(log_folder)


# Create logger
logger = logging.getLogger(app_name)
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()

# File handler
file_handler = logging.FileHandler(log_file_path, mode='a')

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
