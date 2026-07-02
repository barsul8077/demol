import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)

class Config:
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_NAME: str = os.getenv('DB_NAME', 'sanelemonsdb')
    DB_USER: str = os.getenv('DB_USER', 'root')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    INSTAGRAM_BASE_URL: str = os.getenv('INSTAGRAM_BASE_URL', 'https://www.instagram.com')
    SOCIALCAT_URL: str = os.getenv('SOCIALCAT_URL', 'https://thesocialcat.com/tools/instagram-engagement-rate-calculator')
    SCHEDULER_CRON: str = os.getenv('SCHEDULER_CRON', '0 2 * * *')
    LOG_DIR: str = os.getenv('LOG_DIR', 'logs')
    HEADLESS: bool = os.getenv('HEADLESS', 'true').lower() in ('true', '1', 'yes')
    MAX_WORKERS: int = int(os.getenv('MAX_WORKERS', '4'))
    # optional Instagram login
    IG_LOGIN_ENABLED: bool = os.getenv('IG_LOGIN_ENABLED', 'false').lower() in ('true', '1', 'yes')
    IG_USERNAME: str = os.getenv('IG_USERNAME', '')
    IG_PASSWORD: str = os.getenv('IG_PASSWORD', '')
