import logging
import os
from logging.handlers import RotatingFileHandler
from config.config_loader import Config

LOG_DIR = Config.LOG_DIR
os.makedirs(LOG_DIR, exist_ok=True)

def _build_handler(filename: str) -> RotatingFileHandler:
    path = os.path.join(LOG_DIR, filename)
    handler = RotatingFileHandler(path, maxBytes=5_000_000, backupCount=3, encoding='utf-8')
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    )
    return handler

def configure_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not root.handlers:
        root.addHandler(_build_handler('processing.log'))
        root.addHandler(_build_handler('success.log'))
        root.addHandler(_build_handler('error.log'))
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    root.addHandler(console_handler)

logger = logging.getLogger('insta_auto_update')
