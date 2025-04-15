import os
from dsproject.config import OUTPUT_DIR, LOG_PATH
import logging

def create_dirs():
    for folder in ["models", "figures", "reports"]:
        os.makedirs(OUTPUT_DIR / folder, exist_ok=True)

def setup_logging():
    logging.basicConfig(
        filename=LOG_PATH,
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
