from typing import Dict
from database.db_manager import DatabaseManager
from utils.logger import logger

class HistoryManager:
    def __init__(self, db_manager: DatabaseManager) -> None:
        self._db_manager = db_manager

    def create_history(self) -> None:
        self._db_manager.create_history_table()

    def save_history(self, profile_id: int, analysis: Dict[str, any]) -> None:
        try:
            self._db_manager.insert_profile_history(profile_id, analysis)
        except Exception as error:
            logger.error('Failed to save history for profile_id %s: %s', profile_id, error)
