import mysql.connector
from mysql.connector import Error
from typing import Any, Dict, List, Optional
from config.config_loader import Config
from utils.logger import logger

class DatabaseManager:
    def __init__(self) -> None:
        self._test_connection()

    def _connect(self):
        try:
            return mysql.connector.connect(
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                autocommit=False,
            )
        except Error as error:
            logger.error('Database connection failed: %s', error)
            raise

    def _test_connection(self) -> None:
        connection = None
        try:
            connection = self._connect()
            if connection.is_connected():
                logger.info('Connected to MySQL database.')
        finally:
            if connection is not None and connection.is_connected():
                connection.close()

    def fetch_all_usernames(self) -> List[Dict[str, Any]]:
        query = 'SELECT id, username FROM insta_influencers'
        connection = self._connect()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()

    def iter_usernames(self):
        query = 'SELECT id, username FROM insta_influencers'
        connection = self._connect()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
        finally:
            connection.close()

        for record in records:
            yield record

    def fetch_profile_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        query = 'SELECT * FROM insta_influencers WHERE username = %s'
        connection = self._connect()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (username,))
                return cursor.fetchone()
        finally:
            connection.close()

    def update_profile(self, username: str, payload: Dict[str, Any]) -> None:
        columns = ', '.join(f'{key} = %s' for key in payload.keys())
        query = f'UPDATE insta_influencers SET {columns} WHERE username = %s'
        values = list(payload.values()) + [username]
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
            connection.commit()
            logger.info('Updated profile %s', username)
        finally:
            connection.close()

    def insert_profile_history(self, profile_id: int, payload: Dict[str, Any]) -> None:
        query = (
            'INSERT INTO instagram_profile_history '
            '(profile_id, followers, following, posts, engagement_rate, average_likes, average_comments, created_at) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())'
        )
        values = (
            profile_id,
            payload.get('followers'),
            payload.get('following'),
            payload.get('posts'),
            payload.get('engagement_rate'),
            payload.get('average_likes'),
            payload.get('average_comments'),
        )
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
            connection.commit()
            logger.info('Inserted history for profile_id %s', profile_id)
        finally:
            connection.close()

    def create_history_table(self) -> None:
        query = (
            'CREATE TABLE IF NOT EXISTS instagram_profile_history ('
            'id INT AUTO_INCREMENT PRIMARY KEY, '
            'profile_id INT NOT NULL, '
            'followers BIGINT NULL, '
            'following BIGINT NULL, '
            'posts BIGINT NULL, '
            'engagement_rate DECIMAL(8,4) NULL, '
            'average_likes BIGINT NULL, '
            'average_comments BIGINT NULL, '
            'created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, '
            'FOREIGN KEY (profile_id) REFERENCES insta_influencers(id) '
            'ON DELETE CASCADE ON UPDATE CASCADE'
            ')'
        )
        connection = self._connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
            logger.info('Ensured instagram_profile_history table exists.')
        finally:
            connection.close()

    def close(self) -> None:
        logger.info('DatabaseManager does not hold persistent connections to close.')
